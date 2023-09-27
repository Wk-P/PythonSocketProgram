# leat connections

import aiohttp
import asyncio
from aiohttp import web

route_table = [
    {
        "address": "http://127.0.0.1:9011",
        'status': "Y"
    },
    {
        "address": "http://127.0.0.1:9012",
        'status': "Y"
    }
]

# connection counter dictionary
connection_count = {route['address']: 0 for route in route_table}

async def handle_request(request):
    global connection_count

    # find the sum of connections is min
    min_connections_server = min(connection_count, key=connection_count.get)
    server_url = min_connections_server

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=server_url,
            headers=request.headers,
            data=await request.read()
        ) as response:
            response_data = await response.read()
            forwarded_response = web.Response(
                body=response_data,
                status=response.status,
                headers=response.headers
            )

            # add targeted server sum
            connection_count[min_connections_server] += 1

            # release server for reusing
            request.app.loop.call_later(
                1, decrease_connection_count, min_connections_server
            )

            return forwarded_response

def decrease_connection_count(server_url):
    global connection_count
    connection_count[server_url] -= 1

app = web.Application()
app.router.add_post('/', handle_request)
web.run_app(app, host='localhost', port=8081)
