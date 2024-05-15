import requests
import concurrent.futures
import time
import typing
import pandas as pd
import random


def send(n):
    try:
        host = "192.168.56.107"
        port = 8081

        headers = {"task_type": "C"}
        data = {"number": n}

        start = time.time()
        response: dict = requests.post(
            url=f"http://{host}:{port}", headers=headers, data=data
        ).json()

        res = {
            "ip": response.get("ip"),
            "number": n,
            "run-time": time.time() - start,
        }

        usages = response.get("usages")
        if response.get("success") and usages is not None:
            res.update(usages)
            return res
        else:
            return res
    except Exception as e:
        print(e)


def process(requests_sum):
    results = dict()
    print("Request proces start")
    with concurrent.futures.ProcessPoolExecutor() as e:
        futures: typing.List[concurrent.futures.Future] = []
        while requests_sum > 0:
            requests_n = random.randint(1, max(int(requests_sum / 10), 2))
            for _ in range(requests_n):
                futures.append(e.submit(send, random.randint(0, 5000000)))
            requests_sum -= requests_n
            time.sleep(random.randint(4, 10))

        for future in concurrent.futures.as_completed(futures):
            result: dict = future.result()

            for key in result.keys():
                if key not in results.keys():
                    results[key] = list()
                results[key].append(result[key])

    return results


if __name__ == "__main__":
    requests_sum = 100
    results = process(requests_sum)

    df = pd.DataFrame(results)

    excel_writer = pd.ExcelWriter("output.xlsx", engine="openpyxl")
    df.to_excel(excel_writer, index=False, sheet_name="Sheet1")
    excel_writer.close()
