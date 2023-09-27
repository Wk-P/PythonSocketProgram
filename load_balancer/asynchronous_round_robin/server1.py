import aiohttp
import asyncio
from aiohttp import web

async def recur_fibo(n):
    if n <= 1:
        return n
    else:
        return await asyncio.gather(recur_fibo(n-1), recur_fibo(n-2))

async def handle_request(request):
    data = await request.json()
    num = data['num']
    result = await recur_fibo(num)

    response_data = {
        "num": num,
        "result": len(result),
        "host": ":127.0.0.1",
        "port": 9001
    }
    return web.json_response(response_data)

app = web.Application()
app.router.add_post('/', handle_request)

web.run_app(app, host='localhost', port=9001)
