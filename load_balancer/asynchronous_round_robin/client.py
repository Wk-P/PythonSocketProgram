# round robin

import requests
import multiprocessing
import random
import json

server_url = "http://localhost:8080"

def send_request(count, response_counts, lock):
    try:
        data = {
            'num': count
        }
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            print("Request was successful. Server response:")
            json_data = json.loads(response.text)
            print(json_data, end='\n-----\n')
            port = json_data['port']
            
            # 在访问共享的dict前加锁
            with lock:
                if port not in response_counts:
                    response_counts[port] = 1
                else:
                    response_counts[port] += 1
        else:
            print(f"Request failed with status code: {response.status_code}")
    
    except Exception as e:
        print(f"Request failed with error: {str(e)}")

if __name__ == "__main__":
    # 使用Manager创建共享的dict
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    
    # 创建锁
    lock = manager.Lock()

    # 创建多个进程池，并运行send_request函数
    num_processes = 4  # 您可以根据需要更改进程数量
    pool = multiprocessing.Pool(processes=num_processes)
    
    # 创建要发送的请求数量列表
    num_requests = 50
    request_counts = [random.randint(3, 19) for _ in range(num_requests)]
    
    # 使用进程池并发发送请求
    results = []
    
    for count in request_counts:
        if len(results) >= num_processes:
            results.pop(0).get()  # 等待一个进程完成
        result = pool.apply_async(send_request, (count, response_counts, lock))
        results.append(result)
    
    # 等待所有进程完成
    pool.close()
    pool.join()
    
    print("Response counts:")
    for port, count in response_counts.items():
        print(f"Server port {port}: {count} responses")
