import jsonlines


if __name__ == "__main__":
    file_path = "./results_v1_1.jsonl"
    lines = []
    with jsonlines.open(file_path, 'r') as f:
        for line in f:
            lines.append(line)

    for i in lines[500]:
        print(i, "=>", lines[500][i])