import jsonlines

file_name = 'results_v1_4.jsonl'
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
    type_set = set()
    for result in results:
        for key in list(result['replicas_resources']['cpu'].keys()):
            hostname_set.add(key)
        type_set.add(result['type'])

        result['replicas_resources']['cpu'] = {k: result['replicas_resources']['cpu'][k] for k in sorted(result['replicas_resources']['cpu'])}
        result['replicas_resources']['mem'] = {k: result['replicas_resources']['mem'][k] for k in sorted(result['replicas_resources']['mem'])}
        result['replicas_resources']['hdd'] = {k: result['replicas_resources']['hdd'][k] for k in sorted(result['replicas_resources']['hdd'])}
    hostname_one_hot = generate_one_hot_list(len(hostname_set), hostname_set)
    type_one_hot = generate_one_hot_list(len(type_set), type_set)

    w_lines = []

    for result in results:
        response_time = result['data']['runtime']
        hostname = result['hostname']
        req_type = result['type']
        response_sever_code = hostname_one_hot[hostname]
        type_code = type_one_hot[req_type]
        cpu_vec = " ".join(str(x) for x in list(result['replicas_resources']['cpu'].values()))
        mem_vec = " ".join(str(x) for x in list(result['replicas_resources']['mem'].values()))
        hdd_vec = " ".join(str(x) for x in list(result['replicas_resources']['hdd'].values()))
        w_lines.append(f"{response_time} | {response_sever_code} | {cpu_vec} | {mem_vec} | {hdd_vec} | {type_code}\n")
        
    with open(parent_dir + "trainingDataSet_v2.txt", 'w', encoding='utf-8') as wf:
        for wl in w_lines:
            wf.write(wl)

if __name__ == "__main__":
    handler(parent_dir + file_name)