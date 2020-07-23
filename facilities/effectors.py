"""
facilities:effectors
"""

from typing import Dict
from typing import List
from typing import Any

from radiality import effect
from radiality import Effector


class Gate(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def requesting(self, params: Dict[str, Any]) -> None:
        """
        TODO: Add docstring
        """
        self._setup_facility(facility=params.get('facility'))

        if self._is_ready():
            await self._find_facilities()


class CityArea(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def found(self, city_area: List[str]) -> None:
        """
        TODO: Add docstring
        """
        self._setup_city_area(city_area)

        if self._is_ready():
            await self._find_facilities()


class Engine(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def started(self) -> None:
        """
        TODO: Add docstring
        """
        self._on_finding()

        if self._is_ready():
            await self._find_facilities()
