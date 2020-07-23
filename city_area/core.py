"""
city_area:core
"""

import asyncio

import requests
from numpy import array_split

import eventer
import effectors


MAX_AREA_COORDS = 50


class CityArea(eventer.CityArea,
               effectors.CityOsmId,
               effectors.Engine):
    """
    The CityArea
    """
    _city_osm_id: int
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

    def _setup_city_osm_id(self, city_osm_id: int) -> None:
        """
        TODO: Add docstring
        """
        self._city_osm_id = city_osm_id

    def _on_finding(self) -> None:
        """
        TODO: Add docstring
        """
        self._in_finding = True

    def _clean_state(self) -> None:
        """
        TODO: Add docstring
        """
        self._city_osm_id = 0
        self._in_finding = False

    def _is_ready(self) -> bool:
        """
        TODO: Add docstring
        """
        return self._city_osm_id and self._in_finding

    async def _find_city_area(self) -> None:
        """
        TODO: Add docstring
        """
        response = requests.get(
            'http://polygons.openstreetmap.fr/get_geojson.py',
            params={'id': str(self._city_osm_id)}
        )

        geometry = response.json().get('geometries', [{}])
        coordinates = geometry[0].get('coordinates', [[None]])
        original_area = coordinates[0][0]
        if original_area is not None:
            original_area = [
                f'{lat},{lon}' for (lon, lat) in original_area
            ]
            simplified_area = [
                chunk[0]
                for chunk in array_split(original_area, MAX_AREA_COORDS)
            ]
            if simplified_area[0] != simplified_area[-1]:
                simplified_area[-1] = simplified_area[0]

            # Causes the `found` event
            await self.found(city_area=simplified_area)
