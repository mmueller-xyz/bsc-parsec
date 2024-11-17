# BSc Parsec Project

This repository contains the code and resources for the Bachelor's thesis project on the evaluation of the PARSEC benchmark suite in the Vienna Scientific Cluster.

## Overview

The PARSEC (Princeton Application Repository for Shared-Memory Computers) benchmark suite is a collection of parallel programs used for performance studies of multiprocessor systems. This project involves analyzing and working with the PARSEC benchmarks to evaluate and enhance system performance.

## Repository Structure

- `bin/`: Contains executable scripts and binaries.
- `out/`: Directory for output files and results.
- `.gitignore`: Specifies files and directories to be ignored by Git.
- `Makefile`: Build automation tool to generate SLURM job files and run the benchmarks.

## Getting Started

To set up and run the PARSEC benchmarks:

0. **Clone the Parsec Repository and build the benchmarks**:
    ```bash
   git clone https://github.com/bamos/parsec-benchmark
   cd parsec-benchmark
   bin/parsecmgmt  -a build -p blackscholes -c gcc-openmp
   bin/parsecmgmt  -a build -p bodytrack -c gcc-openmp
   bin/parsecmgmt  -a build -p freqmine -c gcc-openmp
   cd ..
   ```
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mmueller-xyz/bsc-parsec.git
   cd bsc-parsec
   ```
2. **Select Configuration in the Makefile**
To configure the benchmarks, open the `Makefile` and edit the relevant variables directly. The `Makefile` does not accept these configurations through command-line variables, so they must be manually set within the file.
3. **Generate SLURM Job Files**:  
   Once the configuration has been set in the `Makefile`, generate the SLURM scripts by running the following command:  
   ```bash
   make all
    ```
    This will create SLURM job files in the `out/` directory, each corresponding to the specified benchmark configurations. The generated files will include all necessary parameters, such as thread count, binding strategy, and input size, for running the benchmarks on the cluster.
4. **Submit Jobs to the Cluster**:  
   After generating the SLURM job files, submit them to the cluster queue using the following command:  
   ```bash
   make srun
   ```
   The output of the jobs is saved into a new out/ folder created at  `pwd`. This can be changed in the following line in the Makefile:
   ```Makefile
	@echo "#SBATCH --output out/$(PACKAGE)_$(CORES_PER_TASK_printed)_$(CONFIG)_$(bind)_%j.out" >> $@
   ```


### Key Variables to Configure

- **`configurations`**: Specify the PARSEC benchmark to run (e.g., `blackscholes`, `bodytrack`, `freqmine`).
- **`threads`**: Define the list of thread counts to test (e.g., `1 2 4 8 16 32`).
- **`partition`**: Specify the SLURM partition to run the job (e.g., `compute`, `high-memory`).
- **`qos`**: Define the quality of service (QoS) level for the job (e.g., `zen3_0512`, `zen3_1024`, `zen3_2048`).
- **`bind`**: Set the process binding strategy (`close`, `spread`, `none`).
- **`input`**: Select the input size for the benchmark.
- **`time`**: Set the maximum wall-clock time for the job in the format `HH:MM:SS` (e.g., `02:00:00` for 2 hours). Note: The lower this number is, the higher the likelihood the scheduler will run the task sooner, especially when using `idle_qos`.
- **`mail`**: Set the email address to receive notifications about job status (e.g., `user@example.com`).
- **`runs`**: Set the amount of benchmark iterations in each SLURM file.
- **`parsecmgmt`**: Path of the `parsecmgmt` binary.

### Example SLURM Script
```bash
#!/bin/bash
#SBATCH --job-name 'bodytrack_001_gcc-openmp_none' 
#SBATCH --output out/bodytrack_001_gcc-openmp_none_%j.out
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 1
#SBATCH --profile=all
#SBATCH --mem=0
#SBATCH --exclusive
#SBATCH --partition=zen3_0512
#SBATCH --time 40:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=examle@tuwien.ac.at
hostname
echo Testing bodytrack 10 times on 1 cores with 1 parallel executions using input size:native and OMP_PROC_BIND: none
date "+%D %T  %s.%N"
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 1 -p bodytrack &
wait
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 1 -p bodytrack &
wait
date "+%D %T  %s.%N"
```

## Data Processing

The script `bin/extractData.py` requires the dependencies
 - pandas,
 - matplotlib,
 - Jinja2
 - numpy and
 - scipy.

The `*.out` files have to be provided as parameters to `extractData.py`
```bash
bin/extractdata.py `ls out/*.out` 
```
The Tables and Figures get exported to `$PWD/benchmark_results`.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments
 - The PARSEC benchmark suite
 - Vienna Scientific Cluster (VSC): https://vsc.ac.at/
 - Dr. Hunold Sascha
 - [Michael Borko](https://github.com/mborko)
