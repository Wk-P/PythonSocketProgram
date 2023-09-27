# round robin

import aiohttp
import asyncio
from aiohttp import web


route_table = [
    {
        "address": "http://127.0.0.1:9001",
        'status': "Y"
    },
    {
        "address": "http://127.0.0.1:9000",
        'status': "Y"
    }
]

server_index = 0

async def handle_request(request):
    # get request from client 
    global server_index
    server_url = None

    while True:
        if route_table[server_index]['status'] == 'Y':
            server_index = (server_index + 1) % len(route_table)
            server_url = route_table[server_index]['address']
            break

    async with aiohttp.ClientSession() as session:
        
        # request transform to target server and get response from this server
        async with session.request(
            method=request.method,
            url=server_url,
            headers=request.headers,
            data=await request.read()
        ) as response:
            
            # send request to client
            response_data = await response.read()
            forwarded_response = web.Response(
                body=response_data,
                status=response.status,
                headers=response.headers
            )
            return forwarded_response
        
app = web.Application()
app.router.add_post('/', handle_request)

web.run_app(app, host='localhost', port=8080)
