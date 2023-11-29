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
            json_data_list = response.json()
            print(f"test :{json_data_list}")
            for res in json_data_list:
                server = res['server']
                if 'number' in res['data']:
                    # update response_counts with lock
                    with lock:
                        if server not in response_counts:
                            response_counts[server] = 1
                        else:
                            response_counts[server] += 1
            
            response_data_list.append(json_data_list)
            
            for res in json_data_list:
                if 'number' in res['data']:
                    print(res)
            
            # total_user = sum(cpu['times']['user'] for cpu in json_data['data']['cpus'])
            # total_sys = sum(cpu['times']['sys'] for cpu in json_data['data']['cpus'])
            # total_idle = sum(cpu['times']['idle'] for cpu in json_data['data']['cpus'])
            # total_irq = sum(cpu['times']['irq'] for cpu in json_data['data']['cpus'])

            # total_time = ( total_user + total_sys + total_idle + total_irq )
            # print(total_time)
            # total_usage = ((total_user + total_sys) / total_time)

            # print(total_usage)

            
                
        else:
            print(f"Request failed with status code: {response.status_code}")

        end_time = time.time()
        response_time_list.append((end_time - start_time, server))
    except Exception as e:
        print(f"Request failed with error: {str(e)}")




if __name__ == "__main__":
    all_start_time = time.time()
    server_url = "http://192.168.56.107:8080"
    
    # make response_counts dictionary with Manager
    manager = multiprocessing.Manager()
    response_counts = manager.dict()
    response_time_list = manager.list()
    response_data_list = manager.list()

    # create lock
    lock = manager.Lock()

    # process pool
    num_processes = 10  # processes number
    pool = multiprocessing.Pool(processes=num_processes)
    
    # requests
    num_requests = 1
    request_counts = [random.randint(10000, 100000) for _ in range(num_requests)]
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
    
    # add all server node address to set
    nodes = set()
    for response in response_data_list:
        for node in response:
            nodes.add(node['server'])


    with open(file_path, 'w', encoding='utf-8') as f:
        for res in response_data_list:
            input = ""
            # ID number for server node
            # get information of each server in every response
            idle_record = ""
            worker_record = ""
            for n in res:
                # For worker node
                data = n['data']
                Id_number = list(nodes).index(n['server'])
                if 'number' in n['data']:
                    worker_record = f"{data['number']} {data['counter']} {data['mem']} {data['cpuUsage']} {data['runtime']} {Id_number} "
                else:
                    idle_record += f"{data['cpuUsage']} {data['mem']} "
                # For idle node
            worker_record + idle_record

            f.write(f"{worker_record + idle_record}\n")

    all_end_time = time.time()
    # print counter
    print("Response counts:")
    for server, data in response_counts.items():
        print(f"Server {server} responses => {data}")
    print(f"Run time : {all_end_time - all_start_time: .3f} seconds")