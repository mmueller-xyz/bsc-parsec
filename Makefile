threads := 001 002 004 008 016 032 064 128 # 256
partition := zen3_0512
qos := zen3_0512
time := "10:00"
mail := "e11810852@student.tuwien.ac.at"
srun := srun
parsecmgmt := $(HOME)/Benchmarks/parsec/bin/parsecmgmt
input := native
configurations:= blackscholes bodytrack # fmm fft barnes ocean_cp ocean_ncp radiosity raytrace volrend water_nsquared water_spatial

all: $(configurations)

# Number of cpus allocated to each Benchmark
%001.slurm: CORES_PER_TASK = 001
%002.slurm: CORES_PER_TASK = 002
%004.slurm: CORES_PER_TASK = 004
%008.slurm: CORES_PER_TASK = 008
%016.slurm: CORES_PER_TASK = 016
%032.slurm: CORES_PER_TASK = 032
%064.slurm: CORES_PER_TASK = 064
%128.slurm: CORES_PER_TASK = 128
%256.slurm: CORES_PER_TASK = 256

# Number of tasks running at the same time
%001.slurm: TASKS = 1
%002.slurm: TASKS = 1
%004.slurm: TASKS = 1
%008.slurm: TASKS = 1
%016.slurm: TASKS = 1
%032.slurm: TASKS = 1
%064.slurm: TASKS = 1
%128.slurm: TASKS = 1
%256.slurm: TASKS = 1

# Number of benchmark iterations
%001.slurm: RUNS = 32
%002.slurm: RUNS = 32
%004.slurm: RUNS = 32
%008.slurm: RUNS = 32
%016.slurm: RUNS = 32
%032.slurm: RUNS = 32
%064.slurm: RUNS = 32
%128.slurm: RUNS = 32
%256.slurm: RUNS = 32

%.slurm:
	@echo "#!/bin/bash" > $@
	@echo "#SBATCH --job-name '$(PACKAGE)_$(CORES_PER_TASK)_$(CONFIG)' " >> $@
	@echo "#SBATCH --output out/$(PACKAGE)_$(CORES_PER_TASK)_$(CONFIG)_%j.out" >> $@
	@echo "#SBATCH --nodes 1" >> $@
	@echo "#SBATCH --ntasks $(TASKS)" >> $@
	@echo "#SBATCH --cpus-per-task $(CORES_PER_TASK)" >> $@
	@echo "#SBATCH --profile=all" >> $@
	@echo "#SBATCH --partition=$(partition)" >> $@
	@echo "#SBATCH --qos $(qos)" >> $@
	@echo "#SBATCH --time $(time)" >> $@
	@echo "#SBATCH --mail-type=ALL" >> $@
	@echo "#SBATCH --mail-user=$(mail)" >> $@
	@echo "hostname" >> $@
	@echo "echo Testing $(PACKAGE) $(RUNS) times on $(CORES_PER_TASK) cores with $(TASKS) parallel executions using input size:$(input)" >> $@
	@echo "date \"+%D %T  %s.%N\"" >> $@
	@for k in {1..$(RUNS)}; do \
		for i in {1..$(TASKS)}; do \
			echo "/home/fs71695/maxmue/Benchmarks/parsec/bin/parsecmgmt -k -a run -c $(CONFIG)  -i $(input) -n $(CORES_PER_TASK) -p $(PACKAGE) &" >> $@ ;\
		done ;\
		echo "wait" >> $@ ;\
	done
	@echo "date \"+%D %T  %s.%N\"" >> $@

blackscholes: $(addsuffix .slurm,$(addprefix blackscholes-,$(threads)))
blackscholes-%.slurm: PACKAGE=blackscholes
blackscholes-%.slurm: CONFIG=gcc-openmp

bodytrack: $(addsuffix .slurm,$(addprefix bodytrack-,$(threads)))
bodytrack-%.slurm: PACKAGE=bodytrack
bodytrack-%.slurm: CONFIG=gcc-openmp

fft: $(addsuffix .slurm,$(addprefix fft-,$(threads)))
fft-%.slurm: PACKAGE=splash2x.fft
fft-%.slurm: CONFIG=gcc-pthreads

fmm: $(addsuffix .slurm,$(addprefix fmm-,$(threads)))
fmm-%.slurm: PACKAGE=splash2x.fmm
fmm-%.slurm: CONFIG=gcc-pthreads

barnes: $(addsuffix .slurm,$(addprefix barnes-,$(threads)))
barnes-%.slurm: PACKAGE=splash2x.barnes
barnes-%.slurm: CONFIG=gcc-pthreads


ocean_cp: $(addsuffix .slurm,$(addprefix ocean_cp-,$(threads)))
ocean_cp-%.slurm: PACKAGE=splash2x.ocean_cp
ocean_cp-%.slurm: CONFIG=gcc-pthreads


ocean_ncp: $(addsuffix .slurm,$(addprefix ocean_ncp-,$(threads)))
ocean_ncp-%.slurm: PACKAGE=splash2x.ocean_ncp
ocean_ncp-%.slurm: CONFIG=gcc-pthreads


radiosity: $(addsuffix .slurm,$(addprefix radiosity-,$(threads)))
radiosity-%.slurm: PACKAGE=splash2x.radiosity
radiosity-%.slurm: CONFIG=gcc-pthreads
radiosity-%.slurm: time="90:00"


raytrace: $(addsuffix .slurm,$(addprefix raytrace-,$(threads)))
raytrace-%.slurm: PACKAGE=splash2x.raytrace
raytrace-%.slurm: CONFIG=gcc-pthreads
raytrace-%.slurm: time="90:00"


volrend: $(addsuffix .slurm,$(addprefix volrend-,$(threads)))
volrend-%.slurm: PACKAGE=splash2x.volrend
volrend-%.slurm: CONFIG=gcc-pthreads
volrend-%.slurm: time="90:00"

water_nsquared: $(addsuffix .slurm,$(addprefix water_nsquared-,$(threads)))
water_nsquared-%.slurm: PACKAGE=splash2x.water_nsquared
water_nsquared-%.slurm: CONFIG=gcc-pthreads


water_spatial: $(addsuffix .slurm,$(addprefix water_spatial-,$(threads)))
water_spatial-%.slurm: PACKAGE=splash2x.water_spatial
water_spatial-%.slurm: CONFIG=gcc-pthreads
water_spatial-%.slurm: time="90:00"

srun-blackscholes:
	for f in $(shell ls .\/blackscholes*.slurm); do sbatch $${f}; done
srun-fmm:
	for f in $(shell ls .\/fmm*.slurm); do sbatch $${f}; done
srun-fft:
	for f in $(shell ls .\/fft*.slurm); do sbatch $${f}; done
srun:
	for f in $(shell ls .\/*.slurm); do sbatch $${f}; done

.PHONY: clean% $(configurations)
clean-jobs:
	rm -rf *.slurm
clean-outfiles: 
	rm -rf out/*.out
clean: clean-jobs