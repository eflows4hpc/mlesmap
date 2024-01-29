#!/bin/sh
module load dislib/master
export PYTHONPATH=$PWD:$PYTHONPATH

export ComputingUnits=1

worker_working_dir=/gpfs/scratch/bsc21/bsc21395/Dislib/Iceland/workdir
base_log_dir=/gpfs/scratch/bsc21/bsc21395/Dislib/Iceland

queue=debug
time_limit=120
num_nodes=8

# log level off for better performance
enqueue_compss --qos=$queue \
 --log_level=off \
 --tracing=false \
 --job_name=rf \
 --worker_in_master_cpus=0 \
 --jvm_master_opts="-Xms16000m,-Xmx50000m,-Xmn1600m" \
 --max_tasks_per_node=48 \
 --exec_time=$time_limit \
 --num_nodes=$num_nodes \
 --base_log_dir=${base_log_dir} \
 --worker_working_dir=${worker_working_dir} \
 --constraints=highmem \
main.py


