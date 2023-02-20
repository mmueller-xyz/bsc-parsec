#!/bin/bash
#SBATCH --job-name 'blackscholes_16_gcc-openmp' 
#SBATCH --output out/blackscholes_16_gcc-openmp_%j.out
#SBATCH --nodes 1
#SBATCH --ntasks 8
#SBATCH --cpus-per-task 16
#SBATCH --profile=all
#SBATCH --partition=zen3_0512
#SBATCH --qos zen3_0512
#SBATCH --time 10:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=e11810852@student.tuwien.ac.at
hostname
echo Testing blackscholes 4 times on 16 cores using input size:native
date "+%D %T  %s.%N"
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
wait
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
wait
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
wait
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c gcc-openmp  -i native -n 16 -p blackscholes &
wait
date "+%D %T  %s.%N"
