#!/usr/bin/env python3
import sys
import pandas as pd
import numpy as np
import re
import os

verbose = False
log = True
numeric_x_axis = True

def parse_minutes_and_seconds(s: str):
    if re.match("(\d+)m(\d+\.\d+)s", s):
        regex = re.search("(\d+)m(\d+\.\d+)s", s)
        return float(regex.group(1)) * 60 + float(regex.group(2))
    return 0.0

def parsefile(infile):
    node = infile.readline().strip()
    test_info = re.findall("^Testing (\w+) (\d+) times on (\d+) cores with (\d+) parallel executions using input size:(\w+)( and OMP_PROC_BIND: (\w+))?$", infile.readline())
    if not test_info:
        return None  # Return None if the line doesn't match expected format

    name, runs, threads, parallel_executions, input_size, _, bind = test_info[0]
    runs, threads, parallel_executions = map(int, [runs, threads, parallel_executions])

    sum_time = 0
    for line in infile:
        if 'COMPUTETIME' in line:
            time_match = re.search("COMPUTETIME[^\d]+(\d+)", line)
            if time_match:
                sum_time += float(time_match.group(1)) / 1000000
        elif 'real' in line:
            time_match = re.search("real\s+(\d+m\d+\.\d+s)", line)
            if time_match:
                sum_time += parse_minutes_and_seconds(time_match.group(1))

    return (name, threads, parallel_executions, bind, sum_time)

def main():
    results = []
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            result = parsefile(file)
            if result:
                results.append(result)

    df = pd.DataFrame(results, columns=['Benchmark', 'Threads', 'Parallel Executions', 'Bind', 'Total Time'])
    df.to_csv("benchmark_results.csv", index=False)

if __name__ == "__main__":
    main()