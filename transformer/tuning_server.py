import os
import sys
import pdb
import numpy as np
import random
import argparse
import codecs
import pickle
import time
import json
# sys.path.insert(0, '/mnt/kabir/services/queue/')
sys.path.insert(0, '/datadrive/global_files/queue/')

from queue_client import QueueClient
from collections import defaultdict as ddict
from collections import OrderedDict
from pprint import pprint

parser = argparse.ArgumentParser(description='')
parser.add_argument('-port',        required=True)
parser.add_argument('-clear',     	action='store_true')
parser.add_argument('-allclear',    action='store_true')
args = parser.parse_args()

q = QueueClient('http://0.0.0.0:{}/'.format(args.port))
if args.clear:
	q.clear()
if args.allclear:
	q.clear()
	exit(0)

exclude_ids = set([])

src_file = "-m src.main"

# OG pretrained model (l3, h2): 'RUN-datasetadd_jump_50_prims_200_examples_pretrain-blankopFalse-tagembFalse-taghidFalse-epochs150-savemodelTrue-embeddingrandom-dmodel128-dmodel1128-dmodel2128-dff256-decoderlayers3-encoderlayers3-heads2-batchsize64-lr00005-emblr00005-dropout01'
# Pretrained model w/ i/p embs frozen (l3, h4): 'RUNZ-pre-emb1-datasetadd_jump_50_prims_200_examples_pretrain-epochs150-savemodelTrue-embeddingrandom-dmodel128-dmodel1128-dmodel2128-dff256-decoderlayers3-encoderlayers3-heads4-batchsize128-lr00005-emblr00005-dropout01'
# Pretrained model w/ o/p embs frozen (l3, h4): 'RUN-freeze-emb2-datasetadd_jump_50_prims_200_examples_pretrain-epochs150-savemodelTrue-embeddingrandom-dmodel128-dmodel1128-dmodel2128-dff256-decoderlayers3-encoderlayers3-heads4-batchsize64-lr0001-emblr0001-dropout01'
# Finetuned model over OG pretrained model (l3, h2): 'RUNX-pre-nor-enc-dec-datasetadd_jump_no_dup-epochs150-savemodelTrue-embeddingrandom-dmodel128-dmodel1128-dmodel2128-dff256-decoderlayers3-encoderlayers3-heads2-batchsize64-lr0001-emblr0001-dropout01'

pretrained_model_name = 'none'
finetune_data_voc = 'none' # 'add_jump_no_dup'

_emb_lr = [0.0005] # Same as LR ###############################
_batch_size = [64, 128]
_lr = [0.0005, 0.0008, 0.001]
_d_ff = [256]
_d_model = [64, 128]
_encoder_layers = [3]
_decoder_layers = [3] # Same as Encoder layers
_heads = [2]
_dropout = [0.1]

mode = 'train'
dev_set = False
test_set = False
gen_set = True
dev_always = False
test_always = False
gen_always = True
eval_last_n = 1 # <dev/test/gen>_always parameter will override this
evaluation_metric = 'soft'
model_selector_set = 'gen' # val for dev set
dataset = 'add_jump_100_prims_controlled'
project = 'scan-transformer-100-prims-controlled-soft-threshold-10'
epochs = 150

embedding = 'random'
emb_name = 'roberta-base'
freeze_emb = False
freeze_emb2 = False
freeze_transformer_encoder = False
freeze_transformer_decoder = False
freeze_fc = False

show_train_acc = True
save_model = False

# opt = 'adam'
i, count = 0, 0

for dropout in _dropout:
	for d_model in _d_model:
		for d_ff in _d_ff:
			for decoder_layers in _decoder_layers:
				for encoder_layers in _encoder_layers:
					for heads in _heads:
						for batch_size in _batch_size:
							for lr in _lr:
								for emb_lr in _emb_lr:
									config = OrderedDict()
									config['src_file'] = src_file
									config['mode'] = mode
									config['project_name'] = project
									config['model_selector_set'] = model_selector_set
									config['pretrained_model_name'] = pretrained_model_name
									config['finetune_data_voc'] = finetune_data_voc
									config['dev_set'] = dev_set
									config['test_set'] = test_set
									config['gen_set'] = gen_set
									config['dev_always'] = dev_always
									config['test_always'] = test_always
									config['gen_always'] = gen_always
									config['eval_last_n'] = eval_last_n
									config['evaluation_metric'] = evaluation_metric
									config['dataset'] = dataset
									config['epochs'] = epochs
									config['save_model'] = save_model
									config['show_train_acc'] = show_train_acc
									config['embedding'] = embedding
									config['emb_name'] = emb_name
									config['freeze_emb'] = freeze_emb
									config['freeze_emb2'] = freeze_emb2
									config['freeze_transformer_encoder'] = freeze_transformer_encoder
									config['freeze_transformer_decoder'] = freeze_transformer_decoder
									config['freeze_fc'] = freeze_fc
									config['d_model'] = d_model
									config['d_ff'] = d_ff
									config['encoder_layers'] = encoder_layers
									config['decoder_layers'] = encoder_layers ###########################
									config['heads'] = heads
									config['batch_size'] = batch_size
									config['lr'] = lr
									config['emb_lr'] = lr
									config['dropout'] = dropout
									if i not in exclude_ids:
										count += 1
										q.enqueue(config)
										print("Inserting {}".format(count), end='\r')

									i += 1

print('\nInserted {}, Total {} in queue. Complete'.format(count, q.getSize()))