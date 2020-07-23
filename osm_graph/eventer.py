"""
osm_graph:eventer
"""

from radiality import event
from radiality import Eventer


class OsmGraph(Eventer):
    """
    TODO: Add docstring
    """

    @event
    async def graph_constructed(self) -> None:
        """
        TODO: Add docstring
        """

    @event
    async def isochrones_constructed(self) -> None:
        """
        TODO: Add docstring
        """

    @event
    async def isochrones_saved(self) -> None:
        """
        TODO: Add docstring
        """
