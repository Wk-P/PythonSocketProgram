# leat connections

import aiohttp
import asyncio
from aiohttp import web

route_table = [
    {
        "address": "http://127.0.0.1:8082",
        'status': "Y"
    },
    {
        "address": "http://127.0.0.1:8083",
        'status': "Y"
    }
]

# create a counter dictionary on routing server
connection_count = {route['address']: 0 for route in route_table}

async def handle_request(request):
    global connection_count

    # 找到当前连接数最少的服务器
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

            # 增加被选中服务器的连接数
            connection_count[min_connections_server] += 1

            # 减少连接数，以便后续请求能够选择其他服务器
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
