"""
gate:main
"""

from core import Gate


if __name__ == '__main__':
    Gate().cohere('nats', '127.0.0.1', 4222).arise()
