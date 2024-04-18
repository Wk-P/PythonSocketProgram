import asyncio
import aiohttp
import random


# send on request
async def request_post(url, session:aiohttp.ClientSession, headers, data):
    async with session.post(url, headers=headers, data=data) as response:
        data = await response.text()
        return data


# send all requests
async def fetch_all_requests(url, sum_requests):
    type_list = ["C", "M", "H"]  # "C": CPU, "M": Memory, "H": Hard disk
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(sum_requests):
            task_type = random.choice(type_list)
            headers = {"task_type": task_type}
            data = dict()
            if task_type == "C":
                data = {"number": random.randint(30000, 50000)}
            elif task_type == "M":
                data = {
                    "size": int(random.randint(50, 300) * pow(2, 20))
                }  # number of bytes
            elif task_type == "H":
                data = {"foo": 0}
            tasks.append(
                asyncio.create_task(
                    request_post(url, session=session, headers=headers, data=data)
                )
            )
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


if __name__ == "__main__":
    server_url = "http://localhost:3000"
    sum_requests = 100
    results = asyncio.run(fetch_all_requests(url=server_url, sum_requests=sum_requests))
    print(results)
