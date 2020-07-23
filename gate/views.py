"""
gate:views
"""

from sanic.views import HTTPMethodView
from sanic.request import Request
from sanic.response import StreamingHTTPResponse
from sanic.response import stream


class MapView(HTTPMethodView):
    
    async def get(self, request: Request) -> StreamingHTTPResponse:
        return stream(self._streaming, content_type='application/json')

    async def _streaming(self, response: StreamingHTTPResponse) -> None:
        await response.write('[')
        await response.write('{')
        await response.write('"a": 1')
        await response.write('},')
        await response.write('{')
        await response.write('"b": 2')
        await response.write('}')
        await response.write(']')
