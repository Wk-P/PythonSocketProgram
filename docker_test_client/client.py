import requests
import multiprocessing
import random
import json

def send_request(server_url, prime_sum, response_counts, lock):
    try:
        data = {
            'num': prime_sum
        }
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            # print("Request was successful. Server response:")
            json_data = response.json()
            # print(json_data, end='\n-----\n')
            port = json_data['server']

            # update response_counts with lock
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

    server_url = "http://192.168.56.102:8080"
    
    # make response_counts dictionary with Manager
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    
    # create lock
    lock = manager.Lock()

    # process pool
    num_processes = 4  # processes number
    pool = multiprocessing.Pool(processes=num_processes)
    
    # requests
    num_requests = 3000
    request_counts = [random.randint(1, 50) for _ in range(num_requests)]
    
    # response result list
    results = []
    
    for count in request_counts:
        if len(results) >= num_processes:
            results.pop(0).get()  # wait the first response pf requests when request queue is full (max = 4)
        result = pool.apply_async(send_request, (server_url, count, response_counts, lock))
        results.append(result)
    
    # wait all prcesses finishing
    pool.close()
    pool.join()
    
    # print counter
    print("Response counts:")
    for server, data in response_counts.items():
        print(f"Server {server} responses => {data}")
