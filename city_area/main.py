"""
city_area:main
"""

from core import CityArea


if __name__ == '__main__':
    CityArea().cohere('nats', '127.0.0.1', 4222).arise()
