import jsonlines

file_name = 'results_v1_3.jsonl'
parent_dir = r"C:\pythonLocalFile\github\PythonSocketProgram\docker_test_client\utils\result_handler\\"


def generate_one_hot_list(length, data_set:set):
    code_dict = dict()
    data_list = list(data_set)
    for index in range(length):
        hostnamme = data_list[index]
        code_dict[hostnamme] = [1 if i == index else 0 for i in range(length)]

    return code_dict


def handler(path):
    results = list()
    with jsonlines.open(path, 'r') as lines:
        for line in lines:
            results.append(line)

    hostname_set = set()
    for result in results:
        for key in list(result['replicas_resources']['cpu'].keys()):
            hostname_set.add(key)

        result['replicas_resources']['cpu'] = {k: result['replicas_resources']['cpu'][k] for k in sorted(result['replicas_resources']['cpu'])}
        result['replicas_resources']['mem'] = {k: result['replicas_resources']['mem'][k] for k in sorted(result['replicas_resources']['mem'])}
        result['replicas_resources']['hdd'] = {k: result['replicas_resources']['hdd'][k] for k in sorted(result['replicas_resources']['hdd'])}
    host_sum = len(hostname_set)
    hostname_one_hot = generate_one_hot_list(host_sum, hostname_set)

    for result in results:
        response_time = result['data']['runtime']
        hostname = result['hostname']
        response_sever_code = hostname_one_hot[hostname]
        cpu_vec = list(result['replicas_resources']['cpu'].values())
        mem_vec = list(result['replicas_resources']['mem'].values())
        hdd_vec = list(result['replicas_resources']['hdd'].values())
        print(response_time, response_sever_code, cpu_vec, mem_vec, hdd_vec)
        


if __name__ == "__main__":
    handler(parent_dir + file_name)