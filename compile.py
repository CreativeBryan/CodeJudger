import os
import sys
import subprocess

from tqdm import tqdm

print(os.environ.get("MinGWCompile"))

MinGWCompile = os.environ.get("MinGWCompile") + "\\c++.exe"
CodePath = f"Code"

MaxCompileProcess = 20

arg = [
    "-std=c++14",
    "-o2",
    "-Wno-unused-parameter",
    "",  # Code Dir
    "-o",
    ""  # Executable File
]

processes = []

totalTask = 0
for _ in os.walk(CodePath):
    totalTask += 1

print("Total Task is:", totalTask)
input()

for i, e in tqdm(enumerate(os.walk(CodePath)), total=totalTask):
    root, dirs, files = e
    print(i, e)

    for file in files:
        cppPath = f"{root}\\{file}"
        exePath = f"bin\\{root}\\{file}.exe"
        arg[3] = cppPath
        arg[5] = exePath

        os.makedirs(f"bin\\{root}", exist_ok=True)

        print(f"CodePath: {cppPath} ", f"Executable File: {exePath}")
        print(f"Compile Args : {arg}")
        processes.append(subprocess.Popen(
            [MinGWCompile] + arg,
            text=True
        ))

        if len(processes) >= MaxCompileProcess:
            for process in processes:
                process.wait()
                if process.stderr:
                    for line in process.stderr:
                        print(line, file=sys.stderr)
            processes.clear()


