# round robin

import requests
import multiprocessing
import random
import json

server_url = "http://localhost:8081"

def send_request(count, response_counts, lock):
    try:
        data = {
            'num': count
        }
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            print(f"Request was successful. Server response: {json_data}")
            port = json_data['port']
            
            # lock value response_counts
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
    # manager values for response_counts
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    
    # lock of response_counts
    lock = manager.Lock()

    # processes pool
    num_processes = 4  # sum of processes
    pool = multiprocessing.Pool(processes=num_processes)
    
    # request list
    num_requests = 50
    request_counts = [random.randint(3, 19) for _ in range(num_requests)]
    
    # response list
    results = []
    
    for count in request_counts:
        if len(results) >= num_processes:
            results.pop(0).get()  # wait first response finished when request process list is full
        result = pool.apply_async(send_request, (count, response_counts, lock))
        results.append(result)
    
    # all process finished
    pool.close()
    pool.join()
    
    print("Response counts:")
    for port, count in response_counts.items():
        print(f"Server port {port}: {count} responses")
