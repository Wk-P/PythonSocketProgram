import multiprocessing
import random
import time
import aiohttp
import asyncio
import jsonlines

# 初步实现发送不同请求类别

time_f = 0

# send on request
async def request_post(url, session:aiohttp.ClientSession, headers, data):
    global time_f
    start_time = time.time()
    time_f = start_time
    print("Send request timestamp => ", start_time)
    # print(f"HEADERS => {headers}, DATA => {data}")
    async with session.post(url, headers=headers, data=data) as response:
        try:
            data = await response.json()
            data['start_timestamp'] = start_time
            # print(f"HEADERS => {headers}, DATA => {data}")
            data['data']['runtime'] = time.time() - start_time
            data['type'] = headers['task_type']
            data['recv_timestamp'] = time.time()
            print(data)
            return data
        except TypeError as e:
            return {"message": e}


# send all requests
async def fetch_all_requests(url, sum_requests):
    type_list = ["C", "M", "H"] # "C": CPU, "M": Memory, "H": Hard disk
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(sum_requests):
            # task_type = random.choice(type_list)
            task_type = "C"
            headers = {"task_type": task_type}
            data = dict()
            if task_type == 'C':
                data = { "number": random.randint(30000, 70000) }
            elif task_type == 'M':
                data = { "size": int(random.randint(20, 40) * pow(2, 10)) }  # number of bytes 
            elif task_type == 'H':
                data = { "foo": 0 }
            tasks.append(asyncio.create_task(request_post(url, session=session, headers=headers, data=data)))
        results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


if __name__ == "__main__":
    start = time.time()
    server_url = "http://192.168.56.107:8080"
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    response_time_list = manager.list()
    response_data_list = manager.list()

    sum_requests = 2500
    loop = asyncio.new_event_loop()
    results = loop.run_until_complete(fetch_all_requests(url=server_url, sum_requests=sum_requests))
    # print(results)
    loop.close()

    print(f"        Program runing time => {time.time() - start}")
    print(f"Sending cumlative send time => {time_f - start} s")

    with jsonlines.open("./results_v2(CPU).jsonl", 'w') as f:
        for r in results:
            try:
                f.write(r)
            except TypeError as e:
                f.write({"message": str(e)})