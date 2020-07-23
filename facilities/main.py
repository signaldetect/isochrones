"""
facilities:main
"""

from core import Facilities


if __name__ == '__main__':
    Facilities().cohere('nats', '127.0.0.1', 4222).arise()
