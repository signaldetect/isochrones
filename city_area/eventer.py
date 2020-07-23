"""
city_area:eventer
"""

from typing import List

from radiality import event
from radiality import Eventer


class CityArea(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def found(self, city_area: List[str]) -> None:
        """
        TODO: Add docstring
        """
