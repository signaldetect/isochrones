"""
engine:eventer
"""

from radiality import event
from radiality import Eventer


class Engine(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def started(self) -> None:
        """
        TODO: Add docstring
        """

    @event
    async def file_saved(self, filepath: str) -> None:
        """
        TODO: Add docstring
        """
