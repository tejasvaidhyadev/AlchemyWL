# eai job new --account mila.arkil_sandbox --cpu 4 --data mila.arkil_sandbox.workspace:/home/toolkit --env HOME=/home/toolkit --gpu 1 --gpu-mem 16 --image registry.console.elementai.com/snow.gradient_transfer/interactive:latest --mem 64 --name tr3 --preemptable --workdir /home/toolkit/collab/Sequence-Clf-Beta/SANClassifier -- /bin/bash -c "source /home/toolkit/envs/collabenv/bin/activate; python -m src.main -run_name tune_try_1 -num_sensi_per_epoch 1 -sensitivity_variable 10 -epochs 30 -wandb"
import os
import numpy as np
import datetime
import time

src_file = "-m src.main"

gpu_mem = 16

_batch_size = [64]
_lr = [0.0008, 0.001]
_dropout = [0.2]

_hidden_size = [256]
_emb1_size = [128]
_depth = [2]

_seeds= [1729] #list(np.random.randint(low=1000, high=9999, size=5))

_opt= ['adam']

mode = 'train'
dataset = 'unmix_1000'
epochs = 200

project_name = 'wl-alchemy-unmix_1000'
model_name = 'lstm'

# embedding = 'random'
# emb_name = 'roberta-base'

# wandb= True
# debug= False

i, count = 0, 0

for seed in _seeds:
    for depth in _depth:
        for hidden_size in _hidden_size:
            for emb1_size in _emb1_size:
                for dropout in _dropout:
                    for opt in _opt:		
                        for batch_size in _batch_size:			
                            for lr in _lr:
                                emb2_size = emb1_size
                                run_name = 'RUN_' + model_name + '-' + dataset
                                job_name = 'job_' + model_name + '_' + dataset

                                run_name = run_name + '-emb1_size' + str(emb1_size) + '-emb2_size' + str(emb2_size) + '-hidden_size' + str(hidden_size) + '-depth' + str(depth) + '-drop' + str(dropout) + '-opt' + opt + '-bs' + str(batch_size) + '-lr' + str(lr) + '-seed' + str(seed)
                                run_name = run_name + "-" + "-".join(str(datetime.datetime.now()).split())[:-7]
                                
                                py_cmd = 'python -m src.main -run_name ' + run_name + ' -mode ' + mode + ' -dataset ' + dataset + ' -project_name ' + project_name + ' -epochs ' + str(epochs)
                                py_cmd = py_cmd + ' -emb1_size ' + str(emb1_size) + ' -emb2_size ' + str(emb2_size) + ' -hidden_size ' + str(hidden_size) + ' -depth ' + str(depth) + ' -dropout ' + str(dropout) + ' -opt ' + opt + ' -batch_size ' + str(batch_size) + ' -lr ' + str(lr) + ' -seed ' + str(seed)
                                
                                bash_cmd = '"source /home/toolkit/envs/cgenv/bin/activate; ' + py_cmd + '"'

                                job_name = job_name + "_" + "_".join(str(datetime.datetime.now()).split())[:-7].replace("-", "_").replace(":", "_")
                                time.sleep(1)

                                job_cmd = 'eai job new --account mila.arkil_sandbox --cpu 4 --data mila.arkil_sandbox.workspace:/home/toolkit --env HOME=/home/toolkit --gpu 1 --gpu-mem ' + str(gpu_mem) + ' --image registry.console.elementai.com/snow.gradient_transfer/interactive:latest --mem 64 --name ' + job_name + ' --preemptable --workdir /home/toolkit/word_learning/AlchemyWL/lstm -- /bin/bash -c ' + bash_cmd
                                os.system(job_cmd)
                                count += 1

print("Submitted " + str(count) + " jobs!")