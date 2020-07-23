"""
gate:core
"""

from typing import Tuple
from typing import Any
import asyncio

from uvloop import Loop
from sanic import Sanic
from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import StreamingHTTPResponse
from sanic.response import stream

import eventer
import effectors


IS_DEBUG_MODE = True
API_SERVER_HOST = '0.0.0.0'
API_SERVER_PORT = 8080
PBF_CHUNK_SIZE = 8192  # bytes


class Gate(eventer.Gate, effectors.Engine):
    """
    The Gate
    """
    _app: Sanic

    _results: asyncio.Queue

    def __init__(self) -> None:
        super().__init__()

        self._app = Sanic(__name__)
        self._app.debug = IS_DEBUG_MODE

    def arise(self) -> None:
        """
        TODO: Add docstring
        """
        # Registers the API server handlers
        self._app.register_listener(self._init_server, 'before_server_start')
        # Prepares the API server
        server_coro = self._app.create_server(
            host=API_SERVER_HOST,
            port=API_SERVER_PORT,
            return_asyncio_server=True
        )
        loop = asyncio.get_event_loop()
        server_task = asyncio.ensure_future(server_coro, loop=loop)
        # Runs the API server
        server = loop.run_until_complete(server_task)
        server.after_start()

        try:
            self._intro()

            self._results = asyncio.Queue()

            # Serves infinitely
            loop.run_forever()
        except KeyboardInterrupt:
            loop.stop()
        finally:
            self._outro()
            # Exit
            server.before_stop()
            # Wait for server to close
            close_task = server.close()
            loop.run_until_complete(close_task)
            # Complete all tasks on the loop
            for connection in server.connections:
                connection.close_if_idle()
            server.after_stop()

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

    async def _init_server(self, loop: Loop, *args: Tuple[Any]) -> None:
        """
        TODO: Add docstring
        """
        self._app.add_route(self._requesting, '/api/map')

    async def _add_result(self, filepath: str) -> None:
        """
        TODO: Add docstring
        """
        await self._results.put(filepath)

    async def _requesting(self, request: Request) -> StreamingHTTPResponse:
        params = {
            key: values[0] for (key, values) in request.get_args().items()
        }
        # Causes the `requesting` event
        await self.requesting(params=params)

        return stream(self._streaming, content_type='application/protobuf')

    async def _streaming(self, response: StreamingHTTPResponse) -> None:
        filepath = await self._results.get()

        with open(filepath, 'rb') as pbf_file:
            bytes_read = pbf_file.read(PBF_CHUNK_SIZE)
            while bytes_read:
                for byte in bytes_read:
                    await response.write(byte)

                bytes_read = pbf_file.read(PBF_CHUNK_SIZE)

        # Notifies the queue that data has been processed
        self._results.task_done()
