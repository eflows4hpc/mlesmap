""" Copyright (c) . All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY 
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING 
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

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
main_load_model.py


