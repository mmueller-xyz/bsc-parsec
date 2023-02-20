#!/bin/bash
#SBATCH --job-name 'blackscholes_8_gcc-openmp' 
#SBATCH --output out/blackscholes_8_gcc-openmp_%j.out
#SBATCH --nodes 1
#SBATCH --ntasks 16
#SBATCH --cpus-per-task 8
#SBATCH --profile=all
#SBATCH --partition=zen3_0512
#SBATCH --qos zen3_0512
#SBATCH --time 10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=e11810852@student.tuwien.ac.at
hostname
echo Testing blackscholes 2 times on 8 cores using input size:native
date "+%D %T  %s.%N"
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
wait
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 8 -p blackscholes &
wait
date "+%D %T  %s.%N"
