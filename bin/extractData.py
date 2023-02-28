#!/usr/bin/python3
import math
import re
import statistics
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

verbose = False
log = False

def parsefile(infile, outfile=sys.stdout):
    node = infile.readline()[:-1]
    test = infile.readline()
    name = test.split()[1]
    runs = int(test.split()[2])
    threads = int(test.split()[5])
    paralell_executions = int(test.split()[7])
    starttime = infile.readline()[:-1]
    endtime = ""

    if verbose: print(f"{threads}c {paralell_executions}p {runs}s")

    data = []
    dumped = 0

    for line in infile:
        endtime = line[:-1]

        if re.match(".*water.spatial.*", name) or name == "splash2x.barnes":
            if re.match(".*COMPUTETIME[^\d]+(\d+).*", line):
                time = float(re.search(".*COMPUTETIME[^\d]+(\d+).*", line).group(1)) / 1000000
                data.append(time)
        elif name.split('.')[0] == "splash2x" and not re.match(".*water.nsquared.*", name) and not re.match(".*volrend.*", name):
            if re.match("(.*ithout[^\d]*]*)(\d+)", line):
                time = float(re.search("(.*ithout[^\d]*]*)(\d+)", line).group(2)) / 1000000
                data.append(time)
        else:
            if re.match("(real)\s+(.*)", line):
                if dumped == 0:
                    time = parse_minutes_and_seconds(re.search("(real)\s+(.*)", line).group(2))
                    data.append(time)
                else:
                    if verbose: print(f"{name} {threads}c {paralell_executions}p {runs}s: ignored time due to core dump: {line[:-1]}", file=sys.stderr)
                    dumped -= 1

        if not re.match(".*\[PARSEC\].*", line):
            pass

        if re.match(".*CANCELLED AT.*", line):
            print(f"{name} {threads}c {paralell_executions}p {runs}s:\n\t{line[:-1]}", file=sys.stderr)
        if re.match(".*\(core dumped\).*", line):
            dumped += 1
            print(f"{name} {threads}c {paralell_executions}p {runs}s:\n\t{line[:-1]}", file=sys.stderr)

    if verbose: print(starttime, file=outfile)
    if verbose: print(f"{name} on {threads} cores", file=outfile)
    if verbose: print(node, file=outfile)
    if verbose: print(data, file=outfile)
    if verbose: print(f"{statistics.median(data)}s median time")
    if verbose: print(f"{statistics.mean(data)}s mean time")
    if verbose: print(
        f"Total time for {len(data)} executions {sum([max(array) for array in np.array_split(np.array(data), runs)])}s")
    if verbose: print(endtime, file=outfile)
    infile.close()

    return f"{threads}c\n{paralell_executions}p\n{runs}s", np.array(data)


def parse_minutes_and_seconds(s: str):
    if re.match("(\d+)m(\d+\.\d+)s", s):
        regex = re.search("(\d)m(\d+\.\d+)s", s)
        return 0.0 + float(regex.group(1)) * 60 + float(regex.group(2))


def sorted_nicely(l):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('(\d+)', key)]
    return sorted(l, key=alphanum_key)


def generate_runtime_per_task_plot(data, filename, folder="~"):
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
    df = df.astype(float)

    mean = df.mean()
    mean.index = np.arange(1, len(mean) + 1)

    fig, ax = plt.subplots()
    ax.set_ylabel("Runtime per task in seconds")
    fig.set_figwidth(5)
    plt.grid(visible=True, which='both')
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', bottom=False)
    plt.margins(x=0)

    # ax.set_xticks(np.linspace(0,40,6))
    if log: ax.set_yscale('log')

    mean.plot(ax=ax)
    df.boxplot(showfliers=True, ax=ax)
    ax.set_ylim(ymin=0)

    plt.title(filename)
    plt.savefig(folder + filename + "_single.pdf")
    plt.close(fig)
    # plt.show()


def generate_total_runtime_plot(data, filename, folder="~"):
    data_scaled = {}
    for index, line in enumerate(data.items()):
        data_scaled[line[0]] = np.multiply(line[1], math.pow(2, min(index, 5)))

    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data_scaled.items()]))
    df = df.astype(float)

    mean = df.mean()
    mean.index = np.arange(1, len(mean) + 1)

    fig, ax = plt.subplots()
    ax.set_ylabel("Total runtime for 32 tasks in seconds")
    fig.set_figwidth(5)
    plt.grid(visible=True, which='both')
    ax.minorticks_on()
    ax.tick_params(axis='x', which='minor', bottom=False)
    plt.margins(x=0)

    # ax.set_xticks(np.linspace(0,40,6))
    if log: ax.set_yscale('log')

    mean.plot(ax=ax)
    df.boxplot(showfliers=True, ax=ax)
    ax.set_ylim(ymin=0)

    plt.title(filename)
    plt.savefig(folder + filename + "_total.pdf")
    plt.close(fig)
    # plt.show()


def visualize_errors(data, filename, folder="~"):
    data_scaled = {}
    for index, line in enumerate(data.items()):
        data_scaled[line[0]] = 32-len(line[1])

    names = list(data_scaled.keys())
    values = list(data_scaled.values())

    plt.ylabel("Number of benchmarks that have not completed (out of 32)")
    plt.ylim(ymax=32)
    plt.minorticks_on()
    plt.tick_params(axis='x', which='minor', bottom=False)
    plt.bar(range(len(data_scaled)), values, tick_label=names)
    # plt.show()

    plt.title(filename)
    plt.savefig(folder + filename + "_errors.pdf")
    plt.close()


def format_error_string(b_data):
    return [(data[0].split('\n')[0], len(data[1])) for data in b_data.items()]


if __name__ == "__main__":
    if len(sys.argv) == 1:
        parsefile(sys.stdin)
    else:
        files = sorted_nicely(sys.argv[1:])
        data = {}
        for raw in files:
            if verbose: print(f"data: {raw}")
            line_data = parsefile(open(raw))
            if data.get(raw.split("/")[-1].split("_")[0]) is None:
                data[raw.split("/")[-1].split("_")[0]] = {}
            data[raw.split("/")[-1].split("_")[0]][line_data[0]] = line_data[1]

        # if data.get("splash2x.raytrace") is not None:
        #     data["splash2x.raytrace"].pop("256c\n1p\n32s")

        for benchmark, b_data in data.items():
            print(f"{benchmark}: \n{format_error_string(b_data)}")

            visualize_errors(b_data, benchmark, "/home/dev/Desktop/BSC/parsec/data/")
            generate_total_runtime_plot(b_data, benchmark, "/home/dev/Desktop/BSC/parsec/data/")
            generate_runtime_per_task_plot(b_data, benchmark, "/home/dev/Desktop/BSC/parsec/data/")
            # try:
            #     generate_total_runtime_plot(b_data, benchmark, "/home/dev/Desktop/BSC/parsec/")
            #     generate_runtime_per_task_plot(b_data, benchmark, "/home/dev/Desktop/BSC/parsec/")
            # except:
            #     pass
