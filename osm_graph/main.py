"""
osm_graph:main
"""

from core import OsmGraph


if __name__ == '__main__':
    OsmGraph().cohere('nats', '127.0.0.1', 4222).arise()
