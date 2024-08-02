#!/usr/bin/env python3
import sys
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
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

    if (bind == ""):
        return None
        bind = "none"

    times = []
    ex = 0
    for line in infile:
        if 'COMPUTETIME' in line:
            time_match = re.search("COMPUTETIME[^\d]+(\d+)", line)
            if time_match:
                times.append(float(time_match.group(1)) / 1000000)
        elif 'real' in line:
            time_match = re.search("real\s+(\d+m\d+\.\d+s)", line)
            if time_match:
                times.append(parse_minutes_and_seconds(time_match.group(1)))

    sigma = np.std(times)
    mu = np.mean(times)

    return (name, len(times), threads, parallel_executions, bind, sum(times), mu, sigma)

def amdahls_law(p, a):
    """ Amdahl's Law formula to calculate theoretical speedup """
    return 1 / ((1 - a) + (a / p))

def fit_amdahls_law(threads, speedups):
    """ Fit Amdahl's law to the observed data """
    weights = threads  # Weight is directly proportional to the number of threads
    params, _ = curve_fit(amdahls_law, threads, speedups, bounds=(0,1)) #, sigma=1./weights)
    return params

def decimal_formatter(x, pos):
    return f'{x:.0f}'  # Adjust the format as needed

def plot_with_error_bars(benchmark, benchmark_group, directory, measure, ylabel, filename, with_fit=True, absolute=False):
    fig, ax = plt.subplots()
    for bind, bind_group in benchmark_group.groupby('Bind'):
        threads = bind_group['Threads']
        values = bind_group[measure]
        if absolute:
            errors = bind_group['Sigma']
        else:
            errors = values * (bind_group['Sigma'] / bind_group['Mu'])  # Error propagation
        p = plt.errorbar(threads, values, yerr=errors, fmt='o-', label=f"Bind: {bind}")
        
        if with_fit and len(values) > 1 and not absolute:
            f = fit_amdahls_law(threads, values)[0]
            fitted_values = amdahls_law(threads, f)
            plt.plot(threads, fitted_values, '--', label=f"Amdahl's Law (α={f:.3f})", color=p[0].get_color())
    
    if with_fit and not absolute:
        plt.plot(threads, amdahls_law(threads, 1), '--', label=f"Amdahl's Law (α=1)", color="grey")

    
    plt.title(f"{ylabel} for {benchmark}")
    plt.xlabel('Number of Threads')
    plt.ylabel(ylabel)
    plt.xscale('log', base=2)
    ax.xaxis.set_major_formatter(FuncFormatter(decimal_formatter))  # Apply the custom formatter
    if with_fit and not absolute:
        plt.yscale('log', base=2)
        ax.yaxis.set_major_formatter(FuncFormatter(decimal_formatter))  # Apply the custom formatter
    # if absolute:
    #     plt.yscale('log', base=10)
    # elif with_fit:
    #     forward = lambda x: amdahls_law(x, 0.8)
    #     inverse = lambda x: 1/forward(x)
    #     plt.yscale('function', functions=(forward, inverse))
    # else:
    #     plt.yscale('log', base=2)
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{directory}/{filename}")
    plt.close()

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def create_latex_tables(benchmark_group, directory, benchmark):
    runtime_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Formatted Time')
    coefficient_of_variation_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='CV')
    speedup_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Speedup')
    efficiency_table = benchmark_group.pivot(columns=['Threads'], index=['Bind'], values='Efficiency')
    
    latex_time = runtime_table.to_latex(caption=f'Wall Time in HH:MM:SS for {benchmark}', na_rep='--', label=f'tab:time_{benchmark}')
    latex_cv = (coefficient_of_variation_table*100).to_latex(float_format="%.2f", caption=f'Coefficient of variation in \%', na_rep='--', label=f'tab:cv_{benchmark}')
    latex_speedup = speedup_table.to_latex(float_format="%.3f", na_rep='--', caption=f'Observed speedup Sp = T1/Tp for {benchmark}', label=f'tab:speedup_{benchmark}')
    latex_efficiency = efficiency_table.to_latex(float_format="%.3f", caption=f'Observed efficiency Ep = Sp/p for {benchmark}', na_rep='--', label=f'tab:eff_{benchmark}')
    
    with open(f"{directory}/{benchmark}_table.tex", 'w') as f:
        f.write(latex_time)
        f.write(latex_cv)
        f.write(latex_speedup)
        f.write(latex_efficiency)

def main():
    results = []
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            result = parsefile(file)
            if result:
                results.append(result)

    df = pd.DataFrame(results, columns=['Benchmark', 'Sequential Executions', 'Threads', 'Parallel Executions', 'Bind', 'Total Time', 'Mu', 'Sigma'])
    df['CV'] = df['Sigma'] / df['Mu']
    df['Total Time'] = df['Mu'] * df['Sequential Executions']
    df['Formatted Time'] = df['Total Time'].apply(format_time)
    df['Bind'].fillna('default', inplace=True)
    df['Baseline Time'] = df.groupby(['Benchmark', 'Bind'])['Mu'].transform(lambda x: x.iloc[0] * max(df.loc[x.index[0], 'Threads'] *.8, 1))
    df['Speedup'] = df['Baseline Time'] / df['Mu']
    df['Efficiency'] = (df['Speedup'] / df['Threads'])

    df.sort_values(['Benchmark', 'Bind', 'Threads'], inplace=True)
    directory = 'benchmark_results'
    create_directory(directory)

    for benchmark, benchmark_group in df.groupby('Benchmark'):
        create_latex_tables(benchmark_group, directory, benchmark)
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Speedup', 'Speedup', f"{benchmark}_speedup_plot.pdf")
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Efficiency', 'Efficiency', f"{benchmark}_eff_plot.pdf", with_fit=False)
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Mu', 'Execution Time (seconds)', f"{benchmark}_time_plot.pdf", with_fit=True, absolute=True)

    df.to_csv(f"{directory}/combined_benchmark_results.csv", index=False)

    print(df)

if __name__ == "__main__":
    main()