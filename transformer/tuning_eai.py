# eai job new --account mila.arkil_sandbox --cpu 4 --data mila.arkil_sandbox.workspace:/home/toolkit --env HOME=/home/toolkit --gpu 1 --gpu-mem 16 --image registry.console.elementai.com/snow.gradient_transfer/interactive:latest --mem 64 --name tr3 --preemptable --workdir /home/toolkit/collab/Sequence-Clf-Beta/SANClassifier -- /bin/bash -c "source /home/toolkit/envs/collabenv/bin/activate; python -m src.main -run_name tune_try_1 -num_sensi_per_epoch 1 -sensitivity_variable 10 -epochs 30 -wandb"
import os
import numpy as np
import datetime
import time

src_file = "-m src.main"

gpu_mem = 16

_batch_size = [128]
_lr = [0.0003, 0.0005]
_dropout = [0.2]

_d_model = [256]
_d_ffn = [128] # twice of d_model
_heads = [8]
_encoder_layers = [2]
_decoder_layers = [2] # same as enc layers

_seeds= [1729] #list(np.random.randint(low=1000, high=9999, size=5))

_opt= ['adam']

mode = 'train'
dataset = 'unmix_1000'
epochs = 300

project_name = 'wl-alchemy-unmix_1000'
model_name = 'transformer'

# embedding = 'random'
# emb_name = 'roberta-base'

# wandb= True
# debug= False

i, count = 0, 0

for seed in _seeds:
    for encoder_layers in _encoder_layers:
        for decoder_layers in _decoder_layers:
            for d_model in _d_model:
                for d_ffn in _d_ffn:
                    for heads in _heads:
                        for dropout in _dropout:
                            for opt in _opt:		
                                for batch_size in _batch_size:			
                                    for lr in _lr:
                                        run_name = 'RUN_' + model_name + '-' + dataset
                                        job_name = 'job_' + model_name + '_' + dataset

                                        run_name = run_name + '-dmodel' + str(d_model) + '-ffn' + str(d_ffn) + '-heads' + str(heads) + '-enc_lay' + str(encoder_layers) + '-dec_lay' + str(decoder_layers) + '-drop' + str(dropout) + '-opt' + opt + '-bs' + str(batch_size) + '-lr' + str(lr) + '-seed' + str(seed)
                                        run_name = run_name + "-" + "-".join(str(datetime.datetime.now()).split())[:-7]
                                        
                                        py_cmd = 'python -m src.main -run_name ' + run_name + ' -mode ' + mode + ' -dataset ' + dataset + ' -project_name ' + project_name + ' -epochs ' + str(epochs)
                                        py_cmd = py_cmd + ' -d_model ' + str(d_model) + ' -d_ff ' + str(d_ffn) + ' -heads ' + str(heads) + ' -encoder_layers ' + str(encoder_layers) + ' -decoder_layers ' + str(encoder_layers) + ' -dropout ' + str(dropout) + ' -opt ' + opt + ' -batch_size ' + str(batch_size) + ' -lr ' + str(lr) + ' -seed ' + str(seed)
                                        
                                        bash_cmd = '"source /home/toolkit/envs/cgenv/bin/activate; ' + py_cmd + '"'

                                        job_name = job_name + "_" + "_".join(str(datetime.datetime.now()).split())[:-7].replace("-", "_").replace(":", "_")
                                        time.sleep(1)

                                        job_cmd = 'eai job new --account mila.arkil_sandbox --cpu 4 --data mila.arkil_sandbox.workspace:/home/toolkit --env HOME=/home/toolkit --gpu 1 --gpu-mem ' + str(gpu_mem) + ' --image registry.console.elementai.com/snow.gradient_transfer/interactive:latest --mem 64 --name ' + job_name + ' --preemptable --workdir /home/toolkit/word_learning/AlchemyWL/transformer -- /bin/bash -c ' + bash_cmd
                                        os.system(job_cmd)
                                        count += 1

print("Submitted " + str(count) + " jobs!")