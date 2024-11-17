#!/usr/bin/env python3
import sys
import pandas as pd
import re
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from scipy.optimize import curve_fit
from enum import Enum


class FitType(Enum):
    SPEEDUP = 1
    EFFICIENCY = 2
    TIME = 3
    NONE = None


def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"


def format_time_as_seconds(seconds):
    return f"{float(seconds):.2f}"


def parse_minutes_and_seconds(s: str):
    regex = re.search("(\d+)m(\d+\.\d+)s", s)
    if regex:
        return float(regex.group(1)) * 60 + float(regex.group(2))
    return 0.0


def parsefile(infile):
    node = infile.readline().strip()
    test_info = re.findall(
        "^Testing (\w+) (\d+) times on (\d+) cores with (\d+) parallel executions using input size:(\w+)( and OMP_PROC_BIND: (\w+))?$",
        infile.readline())
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

    return (name, len(times), threads, parallel_executions, bind, sum(times), mu, sigma, times)


def amdahls_law(p, a):
    """ Amdahl's Law formula to calculate theoretical speedup """
    return 1 / ((1 - a) + (a / p))


def fit_amdahls_law(threads, speedups):
    """ Fit Amdahl's law to the observed data """
    weights = threads  # Weight is directly proportional to the number of threads
    params, _ = curve_fit(amdahls_law, threads[:4], speedups[:4], bounds=(0, 1))
    return params


def decimal_formatter(x, pos):
    return f'{x:.0f}'  # Adjust the format as needed


def plot_with_error_bars(benchmark, benchmark_group, directory, measure, ylabel, filename, with_fit: FitType,
                         absolute=False, with_errors: bool = False):
    fig, ax = plt.subplots()
    for bind, bind_group in benchmark_group.groupby('Bind'):
        threads = bind_group['Threads']
        values = bind_group[measure]

        if with_errors:
            if with_fit == FitType.TIME:
                errors = bind_group['Sigma']
            elif with_fit == FitType.SPEEDUP:
                errors = values * (bind_group['Sigma'] / bind_group['Mu'])  # Error propagation
            p = plt.errorbar(threads, values, yerr=errors, fmt='o-', label=f"Bind: {bind}")
        else:
            p = plt.errorbar(threads, values, fmt='o-', label=f"Bind: {bind}")

        if with_fit != FitType.NONE:
            alpha = bind_group['Alpha'].values[0]  # Use the first Alpha value for plotting
            if with_fit == FitType.SPEEDUP:
                plt.plot(threads, amdahls_law(threads, alpha), '--', label=f"Amdahl's Law (α={alpha:.3f})",
                         color=p[0].get_color())
            elif with_fit == FitType.EFFICIENCY:
                plt.plot(threads, amdahls_law(threads, alpha) / threads, '--', label=f"Amdahl's Law (α={alpha:.3f})",
                         color=p[0].get_color())

    if with_fit != FitType.NONE:
        alpha = 1  # Use the first Alpha value for plotting
        if with_fit == FitType.SPEEDUP:
            plt.plot(threads, amdahls_law(threads, alpha), '--', label=f"Amdahl's Law (α=1)", color="grey")
        elif with_fit == FitType.EFFICIENCY:
            plt.plot(threads, amdahls_law(threads, alpha) / threads, '--', label=f"Amdahl's Law (α=1)", color="grey")

    plt.title(f"{ylabel} for {benchmark}", fontsize=16)
    plt.xlabel('Number of Threads', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)
    plt.xscale('log', base=2)
    ax.xaxis.set_major_formatter(FuncFormatter(decimal_formatter))  # Apply the custom formatter
    if with_fit != FitType.NONE and not absolute:
        plt.yscale('log', base=2)
        ax.yaxis.set_major_formatter(FuncFormatter(decimal_formatter))  # Apply the custom formatter
    ax.tick_params(axis='both', which='major', labelsize=14)
    plt.legend(fontsize=12)
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

    latex_time = runtime_table.to_latex(caption=f'Wall Time in HH:MM:SS for {benchmark}', na_rep='--',
                                        label=f'tab:time_{benchmark}')
    latex_cv = (coefficient_of_variation_table * 100).to_latex(float_format="%.2f",
                                                               caption=f'Coefficient of variation in \%', na_rep='--',
                                                               label=f'tab:cv_{benchmark}')
    latex_speedup = speedup_table.to_latex(float_format="%.3f", na_rep='--',
                                           caption=f'Observed speedup Sp = T1/Tp for {benchmark}',
                                           label=f'tab:speedup_{benchmark}')
    latex_efficiency = efficiency_table.to_latex(float_format="%.3f",
                                                 caption=f'Observed efficiency Ep = Sp/p for {benchmark}', na_rep='--',
                                                 label=f'tab:eff_{benchmark}')

    with open(f"{directory}/{benchmark}_table.tex", 'w') as f:
        f.write(latex_time)
        f.write(latex_cv)
        f.write(latex_speedup)
        f.write(latex_efficiency)

    with open(f"{directory}/{benchmark}_raw_times.tex", "w") as f:
        subtables = []
        for bind_value, bind_group in benchmark_group.groupby('Bind'):
            # Apply the formatting function to each element in the 'Times' list
            bind_group = bind_group.copy()
            bind_group['Times'] = bind_group['Times'].apply(
                lambda times_list: [format_time_as_seconds(time) for time in times_list]
            )

            # Expand 'Times' column into a DataFrame where each column is one run (formatted)
            expanded_times = pd.DataFrame(bind_group['Times'].tolist(), index=bind_group['Threads'])

            # Set the columns to reflect the run number
            expanded_times.columns = [f'{i + 1}' for i in range(expanded_times.shape[1])]

            # Set the index name to 'Threads'
            expanded_times.index.name = 'P{\\textbackslash}Run'

            # Generate LaTeX table code without the table environment
            latex_subtable = expanded_times.to_latex(
                index=True,
                escape=False,
                column_format='l' + 'c' * expanded_times.shape[1]
            )

            # Adjust the LaTeX code to use 'tabularx' for automatic width adjustment
            latex_subtable = latex_subtable.replace('\\begin{tabular}', '\\begin{tabularx}{\\linewidth}')
            latex_subtable = latex_subtable.replace('\\end{tabular}', '\\end{tabularx}')

            # Replace column specifiers with 'X' for 'tabularx'
            num_columns = expanded_times.shape[1] + 1  # +1 for the index column
            original_column_format = 'l' + 'c' * (num_columns - 1)
            column_spec = 'X' * num_columns
            latex_subtable = latex_subtable.replace(
                f'{{{original_column_format}}}',
                f'{{{column_spec}}}'
            )

            # Add a sub-caption for each subtable
            latex_subtable = (
                '\\begin{center}\n'
                f'\\textbf{{Bind {bind_value}}}\n'
                f'{latex_subtable}\n'
                '\\end{center}\n'
            )

            subtables.append(latex_subtable)

        # Combine the subtables into one table environment
        latex_table = '\\begin{table}[htbp]\n'
        latex_table += '\\centering\n'
        latex_table += '{\\fontsize{4pt}{5pt}\\selectfont\n'

        # Add the subtables sequentially
        latex_table += '\n'.join(subtables)
        latex_table += '}\n'

        # Add the main caption and label
        caption = f'Execution time for {benchmark} (seconds)'
        label = f'tab:raw_times_{benchmark}'
        latex_table += f'\\caption{{{caption}}}\n'
        latex_table += f'\\label{{{label}}}\n'
        latex_table += '\\end{table}\n'

        # Write the combined LaTeX table to file
        f.write(latex_table + '\n\n')


def main():
    results = []
    for filename in sys.argv[1:]:
        with open(filename, 'r') as file:
            result = parsefile(file)
            if result:
                results.append(result)

    df = pd.DataFrame(results, columns=['Benchmark', 'Sequential Executions', 'Threads', 'Parallel Executions', 'Bind',
                                        'Total Time', 'Mu', 'Sigma', 'Times'])
    df['CV'] = df['Sigma'] / df['Mu']
    df['Total Time'] = df['Mu'] * df['Sequential Executions']
    df['Formatted Time'] = df['Total Time'].apply(format_time)
    df.fillna({'Bind': 'default'}, inplace=True)
    df['Baseline Time'] = df.groupby(['Benchmark', 'Bind'])['Mu'].transform(
        lambda x: x.iloc[0] * max(df.loc[x.index[0], 'Threads'] * .8, 1))
    df['Speedup'] = df['Baseline Time'] / df['Mu']
    df['Efficiency'] = (df['Speedup'] / df['Threads'])
    alphas = df.groupby(['Benchmark', 'Bind']).apply(
        lambda group: fit_amdahls_law(group['Threads'].values, group['Speedup'].values)[0], include_groups=False
    )
    alphas = alphas.reset_index().rename(columns={0: 'Alpha'})

    # Merge the alpha values back to the original dataframe
    df = pd.merge(df, alphas, on=['Benchmark', 'Bind'])
    df.sort_values(['Benchmark', 'Bind', 'Threads'], inplace=True)
    directory = 'benchmark_results'
    create_directory(directory)

    for benchmark, benchmark_group in df.groupby('Benchmark'):
        create_latex_tables(benchmark_group, directory, benchmark)
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Speedup', 'Speedup',
                             f"{benchmark}_speedup_plot.pdf", FitType.SPEEDUP, with_errors=True)
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Efficiency', 'Efficiency',
                             f"{benchmark}_eff_plot.pdf", FitType.EFFICIENCY, absolute=True)
        plot_with_error_bars(benchmark, benchmark_group, directory, 'Mu', 'Execution Time (seconds)',
                             f"{benchmark}_time_plot.pdf", FitType.TIME, absolute=True, with_errors=True)

    df.to_csv(f"{directory}/combined_benchmark_results.csv", index=False)

    print(df)


if __name__ == "__main__":
    main()
