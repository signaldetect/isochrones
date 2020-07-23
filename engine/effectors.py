"""
engine:effectors
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
        await self._add_job(data=params)


class CityOsmId(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def found(self, city_osm_id: int) -> None:
        """
        TODO: Add docstring
        """
        print('CITY OSM ID FOUND', city_osm_id)


class OsmGraph(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def graph_constructed(self) -> None:
        """
        TODO: Add docstring
        """
        print('GRAPH CONSTRUCTED')

    @effect
    async def isochrones_constructed(self) -> None:
        """
        TODO: Add docstring
        """
        print('ISOCHRONES CONSTRUCTED')

    @effect
    async def isochrones_saved(self) -> None:
        """
        TODO: Add docstring
        """
        print('ISOCHRONES SAVED')
        await self._add_result(is_isochrones_saved=True)


class CityArea(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def found(self, city_area: List[str]) -> None:
        """
        TODO: Add docstring
        """
        print('CITY AREA FOUND', city_area)
