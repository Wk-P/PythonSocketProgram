import aiohttp, aiohttp.web
import asyncio
import json

async def send_request(url, data, headers):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data, headers=headers) as response:
            return await response.json()


async def receive_response():
    while True:
        url = "http://192.168.1.5:8000"
        data = json.dumps({
            "type": "PUSH"
        })
        headers = {
            'Content-Type': 'application/json'
        }
        result = await send_request(url=url, data=data, headers=headers)
        print(result)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(receive_response())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("End request loop!")