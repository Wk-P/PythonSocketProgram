import re


file_name = "hs-log.log"
parent_dir = r"C:\pythonLocalFile\github\PythonSocketProgram\docker_test_client\utils\logs_handler\\"
hostname_set = set()

def generate_one_hot_list(length, data_set:set):
    code_dict = dict()
    data_list = list(data_set)
    for index in range(length):
        hostnamme = data_list[index]
        code_dict[hostnamme] = [1 if i == index else 0 for i in range(length)]

    return code_dict


if __name__ == "__main__":
    with open(parent_dir + file_name, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        hostname = re.findall(r'\[(.+)\]', line)[0]
        hostname_set.add(hostname)


    host_sum = len(hostname_set)
    
    hostname_one_hot = generate_one_hot_list(host_sum, hostname_set)

    print(hostname_one_hot)


    for line in lines:
        print(line.replace('\n', ""))
        host = re.findall(r"\[(.+)\]", line)[0]
        host_code = hostname_one_hot[host]
        mem = re.findall(r"mem: (\d+\.\d+)", line)[0]
        hdd = re.findall(r"hdd: (\d+\.*\d*%)", line)[0]
        timestamp = re.findall(r"timestamp: (\d+\.\d*)", line)[0]
        print(host_code, mem, hdd, timestamp)
        # print(mem)
        # print(hdd)