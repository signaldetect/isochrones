"""
engine:main
"""

from core import Engine


if __name__ == '__main__':
    Engine().cohere('nats', '127.0.0.1', 4222).arise()
