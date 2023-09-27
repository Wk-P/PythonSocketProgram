# weighted

import aiohttp
import asyncio
from aiohttp import web

route_table = [
    {
        "address": "http://127.0.0.1:9021",
        'status': "Y",
        'weight': 3
    },
    {
        "address": "http://127.0.0.1:9022",
        'status': "Y",
        'weight': 2
    }
]

server_index = 0
current_weight = 0

async def handle_request(request):
    global server_index
    global current_weight

    while True:
        # 寻找可用服务器
        server_entry = None
        for _ in range(len(route_table)):
            server_index = (server_index + 1) % len(route_table)
            server_entry = route_table[server_index]
            if server_entry['status'] == 'Y':
                break

        # 计算当前权重
        current_weight -= 1
        if current_weight < 0:
            current_weight = max(entry['weight'] for entry in route_table)

        # 检查是否达到权重要求
        if server_entry['weight'] >= current_weight:
            server_url = server_entry['address']
            break

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
            return forwarded_response

app = web.Application()
app.router.add_post('/', handle_request)

web.run_app(app, host='localhost', port=8082)
