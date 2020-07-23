"""
gate:eventer
"""

from typing import Dict
from typing import Any

from radiality import event
from radiality import Eventer


class Gate(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def requesting(self, params: Dict[str, Any]) -> None:
        """
        TODO: Add docstring
        """
