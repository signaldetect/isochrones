"""
city_osm_id:main
"""

from core import CityOsmId


if __name__ == '__main__':
    CityOsmId().cohere('nats', '127.0.0.1', 4222).arise()
