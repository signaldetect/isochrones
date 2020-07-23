"""
city_osm_id:effectors
"""

from typing import Dict
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

        if self._is_ready():
            await self._find_city()


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
            await self._find_city()
