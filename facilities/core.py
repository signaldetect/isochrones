"""
facilities:core
"""

from typing import List
import os
import asyncio

import requests

import eventer
import effectors


TOMTOM_BASE_URL = 'https://api.tomtom.com/search/2/geometrySearch'
TOMTOM_KEY = os.environ.get('TOMTOM_KEY')


class Facilities(eventer.Facilities,
                 effectors.Gate,
                 effectors.CityArea,
                 effectors.Engine):
    """
    The Facilities
    """
    _facility: str
    _city_area: List[str]
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

    def _setup_facility(self, facility: str) -> None:
        """
        TODO: Add docstring
        """
        self._facility = facility

    def _setup_city_area(self, city_area: List[str]) -> None:
        """
        TODO: Add docstring
        """
        self._city_area = city_area

    def _on_finding(self) -> None:
        """
        TODO: Add docstring
        """
        self._in_finding = True

    def _clean_state(self) -> None:
        """
        TODO: Add docstring
        """
        self._facility = ''
        self._city_area = []
        self._in_finding = False

    def _is_ready(self) -> bool:
        """
        TODO: Add docstring
        """
        return self._facility and self._city_area and self._in_finding

    async def _find_facilities(self) -> None:
        """
        TODO: Add docstring
        """
        response = requests.post(
            f'{TOMTOM_BASE_URL}/{self._facility}.json',
            params={'idxSet': 'POI', 'key': TOMTOM_KEY, 'limit': 100},
            json={
                'geometryList': [
                    {'type': 'POLYGON', 'vertices': self._city_area}
                ]
            }
        )
        results = response.json().get('results', [])
        coords = [
            (
                float(result.get('position', {}).get('lat')),
                float(result.get('position', {}).get('lon'))
            ) for result in results
        ]

        # Causes the `found` event
        await self.found(coords)
