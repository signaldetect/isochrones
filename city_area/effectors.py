"""
city_area:effectors
"""

from typing import Dict
from typing import Any

from radiality import effect
from radiality import Effector


class CityOsmId(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def found(self, city_osm_id: int) -> None:
        """
        TODO: Add docstring
        """
        self._setup_city_osm_id(city_osm_id)

        if self._is_ready():
            await self._find_city_area()


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
            await self._find_city_area()
