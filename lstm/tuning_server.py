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

pretrained_model_name = 'none'
finetune_data_voc = 'none' # 'add_jump_no_dup'

_emb1_size = [64, 128]
_emb2_size = [512] # Same as emb1_size!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
_emb_lr = [0.01] # Same as LR!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
_batch_size = [128, 256]
_lr = [0.005, 0.008, 0.01]
_hidden_size = [64, 128]
_depth = [2]
_dropout = [0.1]

mode = 'train'
dev_set = False
test_set = False
gen_set = False
dev_always = False
test_always = False
gen_always = True
eval_last_n = 1
model_selector_set = 'val' # val for dev set
dataset = 'add_jump_50_prims_controlled'
project = 'grokking-scan-lstm-50-prims-controlled'
epochs = 150

embedding = 'random'
emb_name = 'roberta-base'
freeze_emb = False
freeze_emb2 = False
freeze_lstm_encoder = False
freeze_lstm_decoder = False
freeze_fc = False

show_train_acc = True
save_model = False

# use_attn = True
bidirectional = True
# opt = 'adam'
i, count = 0, 0

for dropout in _dropout:
	for emb1_size in _emb1_size:
		for hidden_size in _hidden_size:
			for depth in _depth: 
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
							config['dataset'] = dataset
							config['epochs'] = epochs
							config['save_model'] = save_model
							config['show_train_acc'] = show_train_acc
							config['bidirectional'] = bidirectional
							config['embedding'] = embedding
							config['emb_name'] = emb_name
							config['freeze_emb'] = freeze_emb
							config['freeze_emb2'] = freeze_emb2
							config['freeze_lstm_encoder'] = freeze_lstm_encoder
							config['freeze_lstm_decoder'] = freeze_lstm_decoder
							config['freeze_fc'] = freeze_fc
							config['emb1_size'] = emb1_size
							config['emb2_size'] = emb1_size #################################################
							config['hidden_size'] = hidden_size
							config['depth'] = depth
							config['batch_size'] = batch_size
							config['lr'] = lr
							config['emb_lr'] = lr #################################################
							config['dropout'] = dropout
							if i not in exclude_ids:
								count += 1
								q.enqueue(config)
								print("Inserting {}".format(count), end='\r')

							i += 1

print('\nInserted {}, Total {} in queue. Complete'.format(count, q.getSize()))