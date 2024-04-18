import requests
import multiprocessing
import random
import json
import time
import aiohttp.web as web
import concurrent.futures



def send_request(args):
    (
        server_url,
        prime_sum,
        response_counts,
        lock,
        response_time_list,
        response_data_list,
    ) = args
    try:
        start_time = time.time()
        data = {"number": prime_sum}
        response = requests.post(server_url, json=data)
        if response.status_code == 200:
            # print("Request was successful. Server response:")
            json_data_list = response.json()

            print(f"Test: {json_data_list}")

            for res in json_data_list:
                server = res["server"]
                if "number" in res["data"]:
                    # update response_counts with lock
                    with lock:
                        if server not in response_counts:
                            response_counts[server] = 1
                        else:
                            response_counts[server] += 1
            response_data_list.append(json_data_list)

        else:
            print(f"Request failed with status code: {response.status_code}")

        end_time = time.time()
        response_time_list.append((end_time - start_time, server))
    except Exception as e:
        print(f"Request failed with error: {str(e)}")


def generate_request_counts():
    cycle = [1]
    while True:
        for count in cycle:
            yield count


if __name__ == "__main__":
    try:
        all_start_time = time.time()
        server_url = "http://192.168.56.107:8080"

        # make response_counts dictionary with Manager
        manager = multiprocessing.Manager()
        response_counts = manager.dict()
        response_time_list = manager.list()
        response_data_list = manager.list()

        # create lock
        lock = manager.Lock()

        # requests
        # cycle_sum = 4
        # num_requests = 1000 * cycle_sum
        num_requests = 3000
        request_counts = [random.randint(40000, 50000) for _ in range(num_requests)]

        # Create cycle loop list for generater
        # request_counts_generator = generate_request_counts()
        futures = []

        with concurrent.futures.ProcessPoolExecutor(max_workers=10) as executor:
            # while num_requests > 0:  # n delta T
                # request_count = next(request_counts_generator)
                # Update sending requests sum
                # num_requests -= request_count

                # if num_requests < 0:
                #     break
            
            # Send requests
            for index in range(num_requests):
                prime_sum = request_counts[index]
                futures.append(
                    executor.submit(
                        send_request,
                        (
                            server_url,
                            prime_sum,
                            response_counts,
                            lock,
                            response_time_list,
                            response_data_list,
                        ),
                    )
                )

                # delta time
                # time.sleep(0.01)

            for future in concurrent.futures.as_completed(futures):
                result = future.result()

        # wait all prcesses finishing
        file_path = "training5-1.txt"

        # add all server node address to set
        nodes = set()
        for response in response_data_list:
            for node in response:
                nodes.add(node["server"])
        with open(file_path, "w", encoding="utf-8") as f:
            for res in response_data_list:
                if res:
                    # get information of each server in every response
                    input = ""
                    idle_record = ""
                    worker_record = ""
                    # for n in res:
                    data = res[0]
                    # For worker node
                    Id_number = list(nodes).index(data["server"])
                    worker_record = f"{data['data']['number']} {data['data']['counter']} {data['data']['runtime']} {Id_number} "
                    idle_record = f"{data['replicas_usage']} "
                    # For idle node
                    record = worker_record + idle_record

                    f.write(f"{record}\n")
    except Exception as e:
        print(e)
    finally:
        all_end_time = time.time()
        # print counter
        print("Response counts:")
        for server in response_counts:
            print(f"Server {server} responses => {response_counts[server]}")
        print(f"Run time : {all_end_time - all_start_time: .3f} seconds")
