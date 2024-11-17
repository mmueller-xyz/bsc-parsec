# BSc Parsec Project

This repository contains the code and resources for the Bachelor's thesis project on the PARSEC benchmark suite.

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
    This will create SLURM job files in the out/ directory, each corresponding to the specified benchmark configurations. The generated files will include all necessary parameters, such as thread count, binding strategy, and input size, for running the benchmarks on the cluster.
4. **Submit Jobs to the Cluster**:  
   After generating the SLURM job files, submit them to the cluster queue using the following command:  
   ```bash
   make submit
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

### Example Configuration

Edit the `Makefile` to set your desired configuration. For example:
```make
configurations=blackscholes
THREADS=001 002 004 008 016 032
BINDING=spread
INPUT=native
```
