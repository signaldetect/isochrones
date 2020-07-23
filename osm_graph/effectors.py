"""
osm_graph:effectors
"""

from typing import Dict
from typing import List
from typing import Tuple
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
        self._setup_place(place=params.get('place'))
        self._setup_trip_time(trip_time=int(params.get('trip_time')))

        if self._is_ready_for_graph_constructing():
            await self._construct_graph()

        if self._is_ready_for_isochrones_constructing():
            await self._construct_isochrones()


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

        if self._is_ready_for_graph_constructing():
            await self._construct_graph()


class Engine(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def started(self) -> None:
        """
        TODO: Add docstring
        """
        self._on_graph_constructing()
        self._on_isochrones_constructing()

        if self._is_ready_for_graph_constructing():
            await self._construct_graph()

        if self._is_ready_for_isochrones_constructing():
            await self._construct_isochrones()


class Facilities(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def found(self, coords: List[Tuple[float, float]]) -> None:
        """
        TODO: Add docstring
        """
        self._setup_facilities(coords)

        if self._is_ready_for_isochrones_constructing():
            await self._construct_isochrones()
