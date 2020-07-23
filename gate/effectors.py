"""
gate:effectors
"""

from radiality import effect
from radiality import Effector


class Engine(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def file_saved(self, filepath: str) -> None:
        """
        TODO: Add docstring
        """
        await self._add_result(filepath)
