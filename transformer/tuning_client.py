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
import subprocess
# sys.path.insert(0, '/mnt/kabir/services/queue/')
sys.path.insert(0, '/datadrive/global_files/queue/')
from queue_client import QueueClient
from collections import defaultdict as ddict
from collections import OrderedDict
from pprint import pprint
# import GPUtil as gputil
thread_num = None

try:
	from subprocess import DEVNULL
except ImportError:
	import os
	DEVNULL = open(os.devnull, 'wb')

def get_cmd(q):
	temp = q.dequeServer()
	if temp == -1:
		print('All Jobs Over!!!!')
		exit(0)
	config = OrderedDict()
	config['src_file'] = temp['src_file']
	config['mode'] = temp['mode']
	config['project_name'] = temp['project_name']
	config['model_selector_set'] = temp['model_selector_set']
	config['pretrained_model_name'] = temp['pretrained_model_name']
	config['finetune_data_voc'] = temp['finetune_data_voc']
	config['dev_set'] = temp['dev_set']
	config['test_set'] = temp['test_set']
	config['gen_set'] = temp['gen_set']
	config['dataset'] = temp['dataset']
	config['dev_always'] = temp['dev_always']
	config['test_always'] = temp['test_always']
	config['gen_always'] = temp['gen_always']
	config['eval_last_n'] = temp['eval_last_n']
	config['evaluation_metric'] = temp['evaluation_metric']
	config['epochs'] = temp['epochs']
	config['save_model'] = temp['save_model']
	config['show_train_acc'] = temp['show_train_acc']
	config['embedding'] = temp['embedding']
	config['emb_name'] = temp['emb_name']
	config['freeze_emb'] = temp['freeze_emb']
	config['freeze_emb2'] = temp['freeze_emb2']
	config['freeze_transformer_encoder'] = temp['freeze_transformer_encoder']
	config['freeze_transformer_decoder'] = temp['freeze_transformer_decoder']
	config['freeze_fc'] = temp['freeze_fc']
	config['d_model'] = temp['d_model']
	config['d_ff'] = temp['d_ff']
	config['decoder_layers'] = temp['decoder_layers']
	config['encoder_layers'] = temp['encoder_layers']
	config['heads'] = temp['heads']
	config['batch_size'] = temp['batch_size']
	config['lr'] = temp['lr']
	config['emb_lr'] = temp['emb_lr']
	config['dropout'] = temp['dropout']

	cmd = 'python {}'.format(config['src_file'])
	del config['src_file']

	run_name = 'RUNS'
	for key, value in config.items():
		if key not in ['project_name', 'model_selector_set', 'pretrained_model_name', 'finetune_data_voc', 'dev_set', 'test_set', 'gen_set', 'show_train_acc', 'emb_name', 'dev_always', 'test_always', 'gen_always', 'eval_last_n', 'evaluation_metric', 'freeze_emb', 'freeze_emb2', 'freeze_transformer_encoder', 'freeze_transformer_decoder', 'freeze_fc']:
			run_name = run_name + '-{}{}'.format(key.replace('_',''), str(value).replace('.',''))
		if key in ['freeze_emb', 'freeze_emb2', 'freeze_transformer_encoder', 'freeze_transformer_decoder', 'freeze_fc', 'results', 'debug', 'save_model', 'show_train_acc', 'dev_set', 'test_set', 'gen_set', 'dev_always', 'test_always', 'gen_always']:
			if key == 'freeze_emb':
				if value == True:
					cmd += ' -freeze_emb'
				else:
					cmd += ' -no-freeze_emb'
			if key == 'freeze_emb2':
				if value == True:
					cmd += ' -freeze_emb2'
				else:
					cmd += ' -no-freeze_emb2'
			if key == 'freeze_transformer_encoder':
				if value == True:
					cmd += ' -freeze_transformer_encoder'
				else:
					cmd += ' -no-freeze_transformer_encoder'
			if key == 'freeze_transformer_decoder':
				if value == True:
					cmd += ' -freeze_transformer_decoder'
				else:
					cmd += ' -no-freeze_transformer_decoder'
			if key == 'freeze_fc':
				if value == True:
					cmd += ' -freeze_fc'
				else:
					cmd += ' -no-freeze_fc'
			if key == 'results':
				if value == True:
					cmd += ' -results'
				else:
					cmd += ' -no-results'
			if key == 'debug':
				if value == True:
					cmd += ' -debug'
				else:
					cmd += ' -no-debug'
			if key == 'save_model':
				if value == True:
					cmd += ' -save_model'
				else:
					cmd += ' -no-save_model'
			if key == 'show_train_acc':
				if value == True:
					cmd += ' -show_train_acc'
				else:
					cmd += ' -no-show_train_acc'
			if key == 'dev_set':
				if value == True:
					cmd += ' -dev_set'
				else:
					cmd += ' -no-dev_set'
			if key == 'test_set':
				if value == True:
					cmd += ' -test_set'
				else:
					cmd += ' -no-test_set'
			if key == 'gen_set':
				if value == True:
					cmd += ' -gen_set'
				else:
					cmd += ' -no-gen_set'
			if key == 'dev_always':
				if value == True:
					cmd += ' -dev_always'
				else:
					cmd += ' -no-dev_always'
			if key == 'test_always':
				if value == True:
					cmd += ' -test_always'
				else:
					cmd += ' -no-test_always'
			if key == 'gen_always':
				if value == True:
					cmd += ' -gen_always'
				else:
					cmd += ' -no-gen_always'
		else:
			cmd += ' -{} {}'.format(key, str(value))

	cmd += ' -run_name {}'.format(run_name)
	return cmd

def gpu_run(q, gpu):
	while True:
		cmd = get_cmd(q)
		cmd += ' -gpu ' + str(gpu)
		print('Command: {}'.format(cmd))
		os.system(cmd)

# def cpu_run(q):
# 	while True:
# 		cmd = '. /scratchd/home/ashutosh/environs/synparcpu/bin/activate;' + get_cmd(q)
# 		print('Command: {}'.format(cmd))
# 		os.system(cmd)

if __name__ == "__main__":

	parser = argparse.ArgumentParser(description='Model Tuner')
	parser.add_argument('-gpu',    default='0')
	parser.add_argument('-port',    required=True)
	parser.add_argument('-cpu',    action='store_true')
	parser.add_argument('-batch',  default=None, 	type=int)
	parser.add_argument('-embed',  default=None, 	type=int)
	args = parser.parse_args()
	batch_size = args.batch
	embed = args.embed
	q = QueueClient('http://0.0.0.0:{}/'.format(args.port))

	if args.cpu:
		cpu_run(q)
	else:
		gpu_run(q, args.gpu)