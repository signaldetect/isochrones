"""
osm_graph:core
"""

from typing import List
from typing import Tuple
from typing import Optional
import asyncio

import osmnx
import networkx
import geopandas
from shapely.geometry import Point
from shapely.geometry import mapping
import fiona

import eventer
import effectors


TRAVEL_SPEED = 4.5  # walking speed in km/hour

osmnx.config(log_console=True, use_cache=True)


class OsmGraph(eventer.OsmGraph,
               effectors.Gate,
               effectors.CityOsmId,
               effectors.Engine,
               effectors.Facilities):
    """
    The OsmGraph
    """
    _place: str
    _trip_time: int
    _city_osm_id: int
    _facilities: List[Tuple[float, float]]
    _in_graph_constructing: bool
    _in_isochrones_constructing: bool

    _graph: Optional[networkx.MultiDiGraph]
    _isochrones: List[geopandas.GeoSeries]

    def __init__(self):
        """
        TODO: Add docstring
        """
        super().__init__()

        self._clean_graph_state()
        self._clean_isochrones_state()

        self._graph = None
        self._isochrones = []

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

    def _setup_trip_time(self, trip_time: int) -> None:
        """
        TODO: Add docstring
        """
        self._trip_time = trip_time

    def _setup_city_osm_id(self, city_osm_id: int) -> None:
        """
        TODO: Add docstring
        """
        self._city_osm_id = city_osm_id

    def _setup_facilities(self, coords: List[Tuple[float, float]]) -> None:
        """
        TODO: Add docstring
        """
        self._facilities = coords

    def _on_graph_constructing(self) -> None:
        """
        TODO: Add docstring
        """
        self._in_graph_constructing = True

    def _on_isochrones_constructing(self) -> None:
        """
        TODO: Add docstring
        """
        self._in_isochrones_constructing = True

    def _clean_graph_state(self) -> None:
        """
        TODO: Add docstring
        """
        self._place = ''
        self._city_osm_id = 0
        self._in_graph_constructing = False

    def _clean_isochrones_state(self) -> None:
        """
        TODO: Add docstring
        """
        self._trip_time = 0
        self._facilities = []
        self._in_isochrones_constructing = False

    def _is_ready_for_graph_constructing(self) -> bool:
        """
        TODO: Add docstring
        """
        return all([
            self._place,
            self._city_osm_id,
            self._in_graph_constructing
        ])

    def _is_ready_for_isochrones_constructing(self) -> bool:
        """
        TODO: Add docstring
        """
        return all([
            self._trip_time,
            self._graph,
            self._facilities,
            self._in_isochrones_constructing
        ])

    async def _construct_graph(self) -> None:
        """
        TODO: Add docstring
        """
        filepath = f'cache/{self._city_osm_id}.graphml'

        try:
            # Tries to load graph
            self._graph = osmnx.load_graphml(filepath=filepath)
        except FileNotFoundError:
            # Downloads the street network
            self._graph = osmnx.graph_from_place(
                self._place, network_type='walk'
            )
            # Caches the graph
            osmnx.save_graphml(self._graph, filepath=filepath)

        self._clean_graph_state()
        # Causes the `graph_constructed` event
        await self.graph_constructed()

    async def _construct_isochrones(self) -> None:
        """
        TODO: Add docstring
        """
        (ys, xs) = list(zip(*self._facilities))
        nodes = osmnx.get_nearest_nodes(self._graph, xs, ys)

        # Projects the graph to UTM
        self._graph = osmnx.project_graph(self._graph)

        # Adds an edge attribute for time in minutes required to traverse each
        # edge
        meters_per_minute = TRAVEL_SPEED * 1000 / 60  # km/hour to m/minute
        for (u, v, k, data) in self._graph.edges(data=True, keys=True):
            data['time'] = data['length'] / meters_per_minute

        # Makes the isochrone polygons for isochrone map
        self._isochrones = []
        for found_node in nodes:
            subgraph = networkx.ego_graph(
                self._graph,
                found_node,
                radius=self._trip_time,
                distance='time'
            )
            node_points = [
                Point((data['x'], data['y']))
                for (node, data) in subgraph.nodes(data=True)
            ]
            bounding_poly = geopandas.GeoSeries(
                node_points
            ).unary_union.convex_hull

            self._isochrones.append(bounding_poly)

        self._clean_isochrones_state()
        # Causes the `isochrones_constructed` event
        await self.isochrones_constructed()
        # Saves data of isochrones
        await self._save_isochrones()

    async def _save_isochrones(self):
        if self._isochrones is not None:
            # Defines a polygon feature geometry with one attribute
            schema = {
                'geometry': 'Polygon',
                'properties': {'id': 'int'}
            }
            poly_id = 0
            with fiona.Env():
                with fiona.open(
                    'data/result.shp', 'w', 'ESRI Shapefile', schema
                ) as shp_file:
                    for bounding_poly in self._isochrones:
                        poly_id += 1
                        shp_file.write({
                            'geometry': mapping(bounding_poly),
                            'properties': {'id': poly_id}
                        })

            # Causes the `isochrones_saved` event
            await self.isochrones_saved()
