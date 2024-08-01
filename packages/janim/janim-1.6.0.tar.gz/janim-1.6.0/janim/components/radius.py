from __future__ import annotations

from functools import lru_cache
from typing import Iterable, Self

import numpy as np

from janim.components.component import Component
from janim.utils.bezier import interpolate
from janim.utils.data import AlignedData, Array
from janim.utils.iterables import resize_with_interpolation


@lru_cache()
def _get_array(radius: float) -> Array:
    array = Array()
    array.data = np.full(1, radius)
    return array


class Cmpt_Radius[ItemT](Component[ItemT]):
    '''
    半径组件，被用于 :class:`DotCloud` 的点半径，以及 :class:`VItem` 的轮廓线粗细
    '''
    def __init__(self, default_radius: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_radius = default_radius

        self._radii = _get_array(self.default_radius).copy()

    def copy(self) -> Self:
        cmpt_copy = super().copy()
        cmpt_copy._radii = self._radii.copy()
        return cmpt_copy

    def become(self, other: Cmpt_Radius) -> Self:
        self.set(other.get())
        return self

    def not_changed(self, other: Cmpt_Radius) -> bool:
        return self._radii.is_share(other._radii)

    @classmethod
    def align_for_interpolate(cls, cmpt1: Cmpt_Radius, cmpt2: Cmpt_Radius):
        len1, len2 = len(cmpt1.get()), len(cmpt2.get())

        cmpt1_copy = cmpt1.copy()
        cmpt2_copy = cmpt2.copy()

        if len1 < len2:
            cmpt1_copy.resize(len2)
        elif len1 > len2:
            cmpt1_copy.resize(len1)

        return AlignedData(cmpt1_copy, cmpt2_copy, cmpt1_copy.copy())

    def interpolate(self, cmpt1: Cmpt_Radius, cmpt2: Cmpt_Radius, alpha: float, *, path_func=None) -> None:
        if cmpt1.not_changed(cmpt2):
            return

        self.set(interpolate(cmpt1.get(), cmpt2.get(), alpha))

    # region 半径数据 | Radii

    def get(self) -> np.ndarray:
        '''
        得到半径数据
        '''
        return self._radii.data

    def set(
        self,
        radius: float | Iterable[float],
        *,
        root_only: bool = False,
    ) -> Self:
        '''
        设置半径数据
        '''
        if not isinstance(radius, Iterable):
            radius = [radius]
        radii = Array()
        radii.data = radius

        for cmpt in self.walk_same_cmpt_of_self_and_descendants_without_mock(root_only):
            cmpt._radii.data = radii

        return self

    def clear(self) -> Self:
        '''
        将半径数据重置为默认值
        '''
        self.set(np.full(1, self.default_radius))

    def reverse(self) -> Self:
        self.set(self.get()[::-1])
        return self

    def resize(self, length: int) -> Self:
        self.set(resize_with_interpolation(self.get(), max(1, length)))
        return self

    def count(self) -> int:
        return len(self.get())

    # endregion
