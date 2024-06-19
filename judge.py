import os
import sys
import subprocess
import re
import threading
import queue
from time import sleep

exePath = "bin"

dataPath = [
    "Data\\T1",
    "Data\\T2",
    "Data\\T3",
    "Data\\T4",
]

MaxRunningProcess = 8

threads = []
exeName = ""


def Judge(prob_name, ans_name, __Name, Q):
    global stderr
    pn = open(prob_name, "rb")
    ans = open(ans_name, "r")

    input_data = pn.read()
    ans_data = [line.rstrip() for line in ans]
    # print(input_data.decode("utf-8"))
    # print(ans_data)
    __process = subprocess.Popen(
        [__Name],
        # ["test.exe"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    try:
        stdout, stderr = __process.communicate(input=input_data, timeout=1)
    except subprocess.TimeoutExpired:
        # print(" --------------------- >>> Judge : " + __Name)
        # print("Time Out", file=sys.stderr)
        __process.kill()
        print(f"Name: {__Name}, Fault in {prob_name} with Time out", file=sys.stderr)
        Q.put((prob_name, 0))
        return
    __process.kill()
    out = stdout.decode('utf-8')
    out = re.compile(r'[\r\n]+').split(out)
    out = out[:len(ans_data)]
    for i in range(len(out)):
        out[i] = out[i].rstrip()

    # print(" --------------------- >>> Judge : " + __Name)
    if out != ans_data:
        # print(f"Wrong Answer: {out}\n org: {stdout}\n Expected: {ans_data}")
        print(f"Name: {__Name}, Fault in {prob_name}", file=sys.stderr)
        Q.put((prob_name, 0))
    else:
        print(f"Correct: {out} :: {stdout}", file=sys.stdout)
        Q.put((prob_name, 1))


def loadExam(data_dir):
    data = []
    ans = []

    for i, (data_root, _, data_names) in enumerate(os.walk(data_dir)):
        for data_name in data_names:
            _, data_ext = os.path.splitext(data_name)
            # print(f"{data_root}\\{data_name}")
            if data_ext == ".in":
                data.append(f"{data_root}\\{data_name}")
            else:
                ans.append(f"{data_root}\\{data_name}")
    # print(f"data: {data}")
    # print(f"ans: {ans}")

    out = [(a, b) for a, b in zip(data, ans)]

    return out


if __name__ == "__main__":

    results = []

    for i, (root, _, names) in enumerate(os.walk(exePath)):
        # if i > 20:
        #     break
        score = 0
        Q = queue.Queue()
        threads = []
        for name in names:
            prob = int(name[1])
            exeName = f"{root}\\{name}"
            print(i, f"{exeName}.", prob)

            for i, (data, ans) in enumerate(loadExam(dataPath[prob - 1])):
                threads.append(threading.Thread(target=Judge, args=(data, ans, exeName, Q)))
                threads[-1].start()

        for thread in threads:
            thread.join()
        # sleep(0.5)
        dets = []
        while not Q.empty():
            qst, s = Q.get()
            score += s
            dets.append((qst, s))
        results.append((root, score, dets))
        print(f"User Name : {root}, Score : {score}", file=sys.stderr)
        print(dets, file=sys.stderr)
        # input()

    F = open("output.csv", "w")
    for root, score, dets in results:
        F.write(f"{root}, {score}, ")
        for qst, s in dets:
            F.write(f"qst: {qst}, score: {s}, ")

        F.write("end\n")


