"""
facilities:eventer
"""

from typing import List
from typing import Tuple

from radiality import event
from radiality import Eventer


class Facilities(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def found(self, coords: List[Tuple[float, float]]) -> None:
        """
        TODO: Add docstring
        """
