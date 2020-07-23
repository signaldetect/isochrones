"""
city_osm_id:core
"""

from typing import Dict
from typing import Any
import asyncio

from geopy.geocoders import Nominatim

import eventer
import effectors


class CityOsmId(eventer.CityOsmId, effectors.Gate, effectors.Engine):
    """
    The CityOsmId
    """
    _place: str
    _in_finding: bool

    def __init__(self):
        """
        TODO: Add docstring
        """
        super().__init__()

        self._clean_state()

    def arise(self) -> None:
        """
        TODO: Add docstring
        """
        loop = asyncio.get_event_loop()

        try:
            self._intro()
            # Runs the infinite event loop only
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self._outro()
            # Exit
            loop.close()

    def _intro(self) -> None:
        """
        TODO: Add docstring
        """
        core_id = self.__class__.__name__
        print(f'(i) The {core_id} core running...')

    def _outro(self) -> None:
        """
        TODO: Add docstring
        """
        core_id = self.__class__.__name__
        print(f'\n(i) The {core_id} core is stopped')

    def _setup_place(self, place: str) -> None:
        """
        TODO: Add docstring
        """
        self._place = place

    def _on_finding(self) -> None:
        """
        TODO: Add docstring
        """
        self._in_finding = True

    def _clean_state(self) -> None:
        """
        TODO: Add docstring
        """
        self._place = ''
        self._in_finding = False

    def _is_ready(self) -> bool:
        """
        TODO: Add docstring
        """
        return self._place and self._in_finding

    async def _find_city(self) -> None:
        """
        TODO: Add docstring
        """
        # Geocoding request via Nominatim
        geolocator = Nominatim(user_agent='city_compare')
        geo_results = geolocator.geocode(
            self._place, exactly_one=False, limit=3
        )

        # Searching for relation in result set
        for result in geo_results:
            print(result.address, result.raw.get('osm_type'))
            if result.raw.get('osm_type') == 'relation':
                city = result
                break

        # Calculating OSM id
        city_osm_id = int(city.raw.get('osm_id'))
        # Cleans
        self._clean_state()

        # Causes the `found` event
        await self.found(city_osm_id)
