import aiohttp
import asyncio
from aiohttp import web
import time

async def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return await asyncio.gather(recur_fibo(n-1), recur_fibo(n-2))

async def handle_request(request):
    data = await request.json()
    num = data['num']
    # asyncio.sleep(0.1)

    response_data = {
        "num": num,
        # "result": result,
        "host": "127.0.0.1",
        "port": 9012
    }
    return web.json_response(response_data)

app = web.Application()
app.router.add_post('/', handle_request)

web.run_app(app, host='127.0.0.1', port=8083)
