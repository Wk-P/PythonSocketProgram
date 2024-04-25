from concurrent.futures import ProcessPoolExecutor
import random
import requests
import time
import jsonlines

def send_request(args):
    url = args[0]
    headers:dict = args[1]
    data:dict = args[2]

    start_time = time.time()
    print(f"Send timestamp => {start_time}")

    response = requests.post(url=url, headers=headers, data=data)
    response_data = response.json()
    response_data['recv_timestamp'] = time.time()
    response_data['send_timestamp'] = start_time
    response_data['type'] = headers.get('task_type')
    response_data["runtime"] = response_data["recv_timestamp"] - start_time
    return response_data

def generate_request():
    st = time.time()
    url="http://192.168.56.107:8080"
    task_type = "C"
    headers = {"task_type": task_type}
    data = {"number": random.randint(30000, 70000)}

    return (url, headers, data)

if __name__ == "__main__":

    program_start_time = time.time()

    sum_requests = 2500   

    request_list = list()
    for _ in range(sum_requests):
        request_list.append(generate_request())

    responses_list = list()

    with ProcessPoolExecutor(max_workers=50) as executor:
        print("- Requests Start -")
        print("- Waiting Responses -")
        results = executor.map(send_request, request_list)

        for result in results:
            responses_list.append(result)

    err_cnt = 0
    suc_cnt = 0

    output_file_path = './response_v1(CPU).jsonl'
    with jsonlines.open(output_file_path, 'w') as f:
        for res in responses_list:
            if "error" in res:
                err_cnt += 1
            else:
                suc_cnt += 1
                f.write(res)
                for k in res:
                    print(f"[{k}] => {res[k]}")
            print("----\n")

    print(f"loss package: {err_cnt}")
    print(f"succ package: {suc_cnt}")
    print(f"        loss: {round(err_cnt / suc_cnt, 4) * 100}%")
    print(f"prog runtime: {time.time() - program_start_time}s")