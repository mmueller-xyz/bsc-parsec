#!/bin/bash
#SBATCH --job-name 'blackscholes_4_gcc-openmp' 
#SBATCH --output out/blackscholes_4_gcc-openmp_%j.out
#SBATCH --nodes 1
#SBATCH --ntasks 32
#SBATCH --cpus-per-task 4
#SBATCH --profile=all
#SBATCH --partition=zen3_0512
#SBATCH --qos zen3_0512
#SBATCH --time 10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=e11810852@student.tuwien.ac.at
hostname
echo Testing blackscholes 1 times on 4 cores using input size:native
date "+%D %T  %s.%N"
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 4 -p blackscholes &
wait
date "+%D %T  %s.%N"
