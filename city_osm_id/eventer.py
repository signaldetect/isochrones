"""
city_osm_id:eventer
"""

from radiality import event
from radiality import Eventer


class CityOsmId(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def found(self, city_osm_id: int) -> None:
        """
        TODO: Add docstring
        """
