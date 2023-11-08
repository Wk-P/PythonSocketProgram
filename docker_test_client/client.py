import requests
import multiprocessing
import random
import json
import time


def send_request(server_url, prime_sum, response_counts, lock, response_time_list, response_data_list):
    try:
        start_time = time.time()
        data = {
            'number': prime_sum
        }
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            # print("Request was successful. Server response:")
            json_data = response.json()
            print(json_data, end='\n-----\n')
            server = json_data['server']

            # update response_counts with lock
            with lock:
                if server not in response_counts:
                    response_counts[server] = 1
                else:
                    response_counts[server] += 1
            
            total_user = sum(cpu['times']['user'] for cpu in json_data['data']['cpus'])
            total_sys = sum(cpu['times']['sys'] for cpu in json_data['data']['cpus'])
            total_idle = sum(cpu['times']['idle'] for cpu in json_data['data']['cpus'])
            total_irq = sum(cpu['times']['irq'] for cpu in json_data['data']['cpus'])
            print(total_user)
            total_time = total_user + total_sys + total_idle + total_irq
            print(total_user)
            print(total_time)
            total_usage = ((total_user + total_sys + total_irq) / total_time)

            response_data_list.append({
                "counter": json_data['data']['counter'],
                "mem": json_data['data']['mem'],
                "cpu": total_usage
                })
        else:
            print(f"Request failed with status code: {response.status_code}")

        end_time = time.time()
        response_time_list.append((end_time - start_time, server))
    except Exception as e:
        print(f"Request failed with error: {str(e)}")




if __name__ == "__main__":
    all_start_time = time.time()
    server_url = "http://192.168.56.102:8080"
    
    # make response_counts dictionary with Manager
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    response_time_list = manager.list()
    response_data_list = manager.list()

    # create lock
    lock = manager.Lock()

    # process pool
    num_processes = 4  # processes number
    pool = multiprocessing.Pool(processes=num_processes)
    
    # requests
    num_requests = 500
    request_counts = [random.randint(1, 10000) for _ in range(num_requests)]
    # response result list
    results = []

    for count in request_counts:
        if len(results) >= num_processes:
            results.pop(0).get()  # wait the first response pf requests when request queue is full (max = 4)
        result = pool.apply_async(send_request, (server_url, count, response_counts, lock, response_time_list, response_data_list))
        results.append(result)
    
    # wait all prcesses finishing
    pool.close()
    pool.join()
    

    file_path = "training.txt"

    with open(file_path, 'w', encoding='utf-8') as f:
        for i in range(num_requests):
            if response_time_list[i][1] == 'http://192.168.56.103:8080':
                vm_name = 1
            elif response_time_list[i][1] == 'http://192.168.56.104:8080':
                vm_name = 0
            # f.write(f"{request_counts[i]} {response_time_list[i][0]} {vm_name} \n")
            f.write(f"{request_counts[i]} {response_data_list[i]['counter']} {response_data_list[i]['mem']} {response_data_list[i]['cpu']} {response_time_list[i][0]} {vm_name} \n")

    all_end_time = time.time()
    # print counter
    print("Response counts:")
    for server, data in response_counts.items():
            print(f"Server {server} responses => {data}")
    print(f"Run time : {all_end_time - all_start_time: .3f} seconds")