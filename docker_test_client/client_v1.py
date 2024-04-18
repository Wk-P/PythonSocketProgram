import multiprocessing
import random
import time
import aiohttp
import asyncio

# 初步实现发送不同请求类别


time_f = 0

# send on request
async def request_post(url, session:aiohttp.ClientSession, headers, data):
    global time_f
    start_time = time.time()
    print("Send request timestamp => ", start_time)
    time_f = start_time
    async with session.post(url, headers=headers, data=data) as response:
        data = await response.json()
        data['data']['runtime'] = time.time() - start_time
        print(data)
        return data


# send all requests
async def fetch_all_requests(url, sum_requests):
    type_list = ["C", "M", "H"] # "C": CPU, "M": Memory, "H": Hard disk
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(sum_requests):
            task_type = random.choice(type_list)
            headers = { "task_type": task_type }
            data = dict()
            if task_type == 'C':
                data = { "number": random.randint(30000, 50000) }
            elif task_type == 'M':
                data = { "size": int(random.randint(500, 1000) * pow(2, 20)) }  # number of bytes 
            elif task_type == 'H':
                data = {"foo": 0}
            tasks.append(asyncio.create_task(request_post(url, session=session, headers=headers, data=data)))
        results = await asyncio.gather(*tasks, return_exceptions=True)
    return results


if __name__ == "__main__":
    server_url = "http://192.168.56.107:8080"
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    response_time_list = manager.list()
    response_data_list = manager.list()

    start = time.time()

    sum_requests = 10
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(fetch_all_requests(url=server_url, sum_requests=sum_requests))
    print(results)
    print(f"Cumlative send time => {time_f - start} s")


    loop.close()