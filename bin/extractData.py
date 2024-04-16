#!/usr/bin/env python3
import sys
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def parse_minutes_and_seconds(s: str):
    regex = re.search("(\d+)m(\d+\.\d+)s", s)
    if regex:
        return float(regex.group(1)) * 60 + float(regex.group(2))
    return 0.0

def parsefile(infile):
    node = infile.readline().strip()
    test_info = re.findall("^Testing (\w+) (\d+) times on (\d+) cores with (\d+) parallel executions using input size:(\w+)( and OMP_PROC_BIND: (\w+))?$", infile.readline())
    if not test_info:
        return None
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
    return (name, runs, threads, parallel_executions, bind, sum_time)

def amdahls_law(p, a):
    """ Amdahl's Law formula to calculate theoretical speedup """
    return 1 / ((1 - a) + (a / p))

def fit_amdahls_law(threads, speedups):
    """ Fit Amdahl's law to the observed data """
    weights = threads  # Weight is directly proportional to the number of threads
    params, _ = curve_fit(amdahls_law, threads, speedups, bounds=(0,1), sigma=1./weights)
    return params

def main():
    results = []
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            result = parsefile(file)
            if result:
                results.append(result)

    df = pd.DataFrame(results, columns=['Benchmark', 'Sequential Executions', 'Threads', 'Parallel Executions', 'Bind', 'Total Time'])
    df['Average Time'] = df['Total Time'] / df['Sequential Executions']
    df['Formatted Time'] = df['Total Time'].apply(format_time)
    df['Bind'].fillna('default', inplace=True)
    df['Baseline Time'] = df.groupby(['Benchmark', 'Bind'])['Total Time'].transform(lambda x: x.iloc[0] * df.loc[x.index[0], 'Threads'])
    df['Speedup'] = df['Baseline Time'] / df['Total Time']
    df['Efficiency'] = (df['Speedup'] / df['Threads'])

    df.sort_values(['Benchmark', 'Bind', 'Threads'], inplace=True)
    print(df)

    directory = 'benchmark_results'
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create plots for each benchmark
    for benchmark, benchmark_group in df.groupby('Benchmark'):        
        runtime_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Formatted Time')
        speedup_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Speedup')
        efficiency_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Efficiency')
        # speedup_table.to_csv(f"{directory}/{benchmark}_speedup.csv", index=False)
        # runtime_table.to_csv(f"{directory}/{benchmark}_runtime.csv", index=False)
        # efficiency_table.to_csv(f"{directory}/{benchmark}_efficiency.csv", index=False)
        latex_time = runtime_table.to_latex(caption=f'Wall Time in HH:MM:SS for {benchmark}', na_rep='--', label=f'tab:time_{benchmark}')
        latex_speedup = speedup_table.to_latex(float_format="%.3f", na_rep='--', caption=f'Observed speedup Sp = T1/Tp for {benchmark}', label=f'tab:speedup_{benchmark}')
        latex_efficiency = efficiency_table.to_latex(float_format="%.3f", caption=f'Observed efficiency Ep = Sp/p {benchmark}', na_rep='--', label=f'tab:eff_{benchmark}')
        with open(f"{directory}/{benchmark}_table.tex", 'w') as f:
            f.write(latex_time)
            f.write(latex_speedup)
            f.write(latex_efficiency)
        plt.figure()
        for bind, bind_group in benchmark_group.groupby('Bind'):
            threads = bind_group['Threads']
            speedups = bind_group['Speedup']
            plt.plot(threads, speedups, 'o-', label=f"Bind: {bind}")
            
            # Fit and plot Amdahl's law
            if len(speedups) > 1:  # We need at least two points to fit
                f = fit_amdahls_law(threads, speedups)[0]
                fitted_speedups = amdahls_law(threads, f)
                plt.plot(threads, fitted_speedups, '--', label=f"Amdahl's Law (α={f:.2f})")
        
        plt.title(f"Speedup for {benchmark}")
        plt.xlabel('Number of Threads')
        plt.ylabel('Speedup')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{directory}/{benchmark}_speedup_plot.png")
        plt.close()

        plt.figure()
        for bind, bind_group in benchmark_group.groupby('Bind'):
            threads = bind_group['Threads']
            speedups = bind_group['Efficiency']
            plt.plot(threads, speedups, 'o-', label=f"Bind: {bind}")
            
            # # Fit and plot Amdahl's law
            # if len(speedups) > 1:  # We need at least two points to fit
            #     f = fit_amdahls_law(threads, speedups)[0]
            #     fitted_speedups = amdahls_law(threads, f)
            #     plt.plot(threads, fitted_speedups, '--', label=f"Amdahl's Law (α={f:.2f})")
        
        plt.title(f"Efficiency for {benchmark}")
        plt.xlabel('Number of Threads')
        plt.ylabel('Efficiency')
        plt.legend()
        plt.grid(True)
        plt.savefig(f"{directory}/{benchmark}_eff_plot.png")
        plt.close()

    df.to_csv(f"{directory}/combined_benchmark_results.csv", index=False)

if __name__ == "__main__":
    main()
