import os
import time
import argparse
import pdb
from filelock import FileLock
import json
import openai
import pandas as pd
from prompts import get_prompt, permute_prompts
import numpy as np

global result_folder
result_folder = './out/'
outputs_folder = 'outputs'

example = 0

def build_parser():
	# Data loading parameters
	parser = argparse.ArgumentParser(description='Run Single sequence model')

	parser.add_argument('-exp_type', type=str, default='multi_sample', help='experiment type')
	parser.add_argument('-run_name', type=str, default='default', help='run name for logs')
	parser.add_argument('-data', type=str, default='gsm8k', help='Which data is being evaluated')
	parser.add_argument('-api_key', type=str, default='microsoft1', help='Which OpenAI API Key to use')
	parser.add_argument('-prompt_type', type=str, default='math_cot_default_mistake_post_indicators_2', help='Which prompt to provide')
	parser.add_argument('-eval_type', type=str, default='math', help='How to obtain final answer')
	parser.add_argument('-check_pred', type=str, default='no', help='Ask model about its own prediction')
	parser.add_argument('-stop_seq', type=str, default=' [', help='When to stop generation')
	parser.add_argument('-indicator_type', type=str, default='post', help='Which type of indicator')
	parser.add_argument('-max_calls_per_ex', type=int, default=25, help='Maximum number of api calls per example')
	parser.add_argument('-model', type=str, default='text-davinci-002', help='Which model to use')
	parser.add_argument('-max_tokens', type=int, default=256, help='Maximum number of tokens')
	parser.add_argument('-temperature', type=float, default=0.3, help='Sampling temperature')
	parser.add_argument('-indi_temperature', type=float, default=0.0, help='Indicator token temperature')
	parser.add_argument('-top_p', type=float, default=1.0, help='top what percentage of tokens to be considered') # Alter this or temp, not both
	parser.add_argument('-n', type=int, default=8, help='number of completions to generate for each prompt')
	parser.add_argument('-presence_penalty', type=float, default=0.0, help='positive values increases model\'s likelihood to talk about new topics')
	parser.add_argument('-frequency_penalty', type=float, default=0.0, help='positive values decreases model\'s likelihood to repeat same line verbatim')
	parser.add_argument('-sleep_btw', type=str, default='yes', help='sleep in between')
	parser.add_argument('-indi_temp', type=str, default='yes', help='indicator temperature different')
	parser.add_argument('-rep_ques', type=str, default='no', help='repeat question')
	parser.add_argument('-time_per_request', type=float, default=1.0, help='Time to be taken per request')
	parser.add_argument('-aggregate', type=str, default='sum', help='how to aggregate log probs of tokens in a step')

	return parser

def create_save_directories(path):
	if not os.path.exists(path):
		os.makedirs(path)

def store_results(config, accuracy):
	with FileLock(config.result_path + '.lock'):
		try:
			with open(config.result_path) as f:
				res_data = json.load(f)
		except:
			res_data = {}

		data= {'run_name' : str(config.run_name)
		, 'dataset': config.data
		, 'accuracy': str(accuracy) 
		, 'model': config.model
		, 'prompt_type': config.prompt_type
		, 'eval_type': config.eval_type
		, 'max_tokens': config.max_tokens
		, 'temperature': config.temperature
		, 'top_p': config.top_p
		, 'n': config.n
		, 'presence_penalty': config.presence_penalty
		, 'frequency_penalty': config.frequency_penalty
		}
		res_data[str(config.run_name)] = data

		with open(config.result_path, 'w', encoding='utf-8') as f:
			json.dump(res_data, f, ensure_ascii= False, indent= 4)

parser = build_parser()
config = parser.parse_args()

if config.run_name == "default":
	config.run_name = config.exp_type + "-" + config.data + "-" + config.prompt_type + "-" + config.model + "-" + str(config.temperature) + "-" + str(config.n) + "-" + config.aggregate

run_name = config.run_name
config.outputs_path = os.path.join(outputs_folder, run_name)
config.result_path = os.path.join(result_folder, 'val_results_{}.json'.format(config.data))

create_save_directories(config.outputs_path)

if config.api_key == "personal":
	openai.api_key = os.getenv("OPENAI_API_KEY_PERSONAL")
elif config.api_key == 'microsoft1':
	openai.api_key = os.getenv("OPENAI_API_KEY_MICROSOFT")
elif config.api_key == 'microsoft2':
	openai.api_key = os.getenv("OPENAI_API_KEY_MICROSOFT2")
elif config.api_key == 'microsoft3':
	openai.api_key = os.getenv("OPENAI_API_KEY_MICROSOFT3")
elif config.api_key == 'microsoft4':
	openai.api_key = os.getenv("OPENAI_API_KEY_MICROSOFT4")
else:
	openai.api_key = config.api_key
openai.Engine.list()

data_path = "data/" + config.data + "/gen.tsv"
test_df = pd.read_csv(data_path, sep="\t")

stop_sequences = [x for x in config.stop_seq.split(";")]

def run_evaluation_with_mistakes_multi_sample(start_ex = 0):
	global example
	corr = 0.0
	tot = 0.0
	max_ex = len(test_df)
	for i in range(start_ex, max_ex):
		base_prompt = get_prompt(i, test_df, config.prompt_type)
		full_response = ""
		corr_response = ""
		qa = "\n".join(base_prompt.split("\n")[-2:])

		with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
			f_out.write('---------------------------------------\n')
			f_out.write('Example: ' + str(i) + '\n')
			f_out.write('Source: ' + test_df.loc[i]["Input"] + '\n')
			f_out.write('---------------------------------------\n')
			f_out.close()

		for j in range(config.max_calls_per_ex):
			with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
				f_out.write('---------------------------------------\n')
				f_out.write('Step: ' + str(j) + '\n')
				f_out.close()
			start_time = time.time()
			# print("base prompt: ", base_prompt)
			# print()
			# print("temp: ", str(temps[indi_flag]))
			# print()
			response = openai.Completion.create(
				engine=config.model,
				prompt=base_prompt,
				max_tokens=config.max_tokens,
				temperature=config.temperature,
				top_p=config.top_p,
				n=config.n,
				stop=stop_sequences,
				presence_penalty=config.presence_penalty,
				frequency_penalty=config.frequency_penalty,
				best_of=config.n+1,
				logprobs=1
			)
			end_time = time.time()
			time_taken = end_time - start_time
			if config.sleep_btw == 'yes' and time_taken < config.time_per_request:
				time.sleep(config.time_per_request-time_taken)
			responses = []
			label_responses = []
			probs = []
			for z in range(len(response["choices"])):
				cur_response = response["choices"][z]["text"].split("\n")[0].strip()
				cur_response_log_probs_arr = np.array(response["choices"][z]["logprobs"]["token_logprobs"])
				if config.aggregate == "sum":
					cur_response_log_probs = np.sum(cur_response_log_probs_arr)
				elif config.aggregate == "average":
					cur_response_log_probs = np.sum(cur_response_log_probs_arr)/len(cur_response_log_probs_arr)
				else:
					cur_response_log_probs = 0.0
				
				if cur_response == "":
					continue
				if cur_response[-1] == ".":
					cur_response = cur_response[:-1]
				temp_base_prompt = base_prompt + " " + cur_response + "."
				corr_label = openai.Completion.create(
					engine=config.model,
					prompt=temp_base_prompt,
					max_tokens=config.max_tokens,
					temperature=config.indi_temperature,
					top_p=config.top_p,
					n=1,
					stop=".",
					presence_penalty=config.presence_penalty,
					frequency_penalty=config.frequency_penalty,
					best_of=1,
					logprobs=1
				)
				corr_label_response = corr_label["choices"][0]["text"].split("\n")[0].strip()

				with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
					f_out.write('---------------------------------------\n')
					f_out.write('generation: ' + cur_response + '\n')
					f_out.write('correctness: ' + corr_label_response + '\n')
					f_out.close()

				if "correct" in corr_label_response and "incorrect" not in corr_label_response:
					responses.append(cur_response)
					label_responses.append(corr_label_response)
					try:
						idx = corr_label["choices"][0]["logprobs"]["tokens"].index(" correct")
					except:
						idx = corr_label["choices"][0]["logprobs"]["tokens"].index("correct")
					label_response_log_probs = corr_label["choices"][0]["logprobs"]["token_logprobs"][idx]
					probs.append(label_response_log_probs + cur_response_log_probs)
					with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
						f_out.write('Step Prob: ' + str(cur_response_log_probs) + '\n')
						f_out.write('Label Prob: ' + str(label_response_log_probs) + '\n')
						f_out.close()
				with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
					f_out.write('---------------------------------------\n')
					f_out.close()

			if len(probs) > 0:
				probs_arr = np.array(probs)
				max_probs = probs_arr.max()
				idx = probs.index(max_probs)
				selected_response = responses[idx]
				selected_label_response = label_responses[idx]

				full_response = full_response + " " + selected_response + ". " + selected_label_response + "."
				corr_response = corr_response + " " + selected_response + ". " + selected_label_response + "."
				base_prompt = base_prompt + " " + selected_response + ". " + selected_label_response + "."

				if "answer" in selected_response:
					break
			else:
				with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
					f_out.write('---------------------------------------\n')
					f_out.write('NONE CORRECT \n')
					f_out.write('---------------------------------------\n')
					f_out.close()

		try:
			if corr_response[-1] == ".":
				corr_response = corr_response[:-1]
		except:
			corr_response = "0.179"
		corr_response = corr_response.replace(",", "")
		corr_response = corr_response.replace("$", "")
		corr_response = corr_response.replace("€", "")
		corr_response = corr_response.replace("%", "")
		num_ls = []
		for t in corr_response.split()[-7:]:
			try:
				num_ls.append(float(t))
			except ValueError:
				pass
		try:
			corr_response = num_ls[-1]
		except:
			corr_response = 0.179

		tot += 1
		disp_corr = 0
		if corr_response == test_df.loc[i]["Output"]:
			corr += 1
			disp_corr = 1

		with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
			f_out.write('---------------------------------------\n')
			f_out.write('Example: ' + str(i) + '\n')
			f_out.write('Source: ' + test_df.loc[i]["Input"] + '\n')
			f_out.write('Target: ' + str(test_df.loc[i]["Output"]) + '\n')
			f_out.write('Generated: ' + str(corr_response) + '\n')
			f_out.write('Result: ' + str(disp_corr) + '\n')
			f_out.write('Full Response: ' + str(full_response) + '\n')
			f_out.write('\n')
			f_out.write('---------------------------------------\n')
			f_out.close()

		print("Completed {} / {}...".format(i+1, max_ex), end = '\r', flush = True)
		example+=1
		# print(example)

	acc = corr/tot
	return acc

def run_evaluation_with_mistakes():
	corr = 0.0
	tot = 0.0
	tp = 0.0
	tn = 0.0
	fp = 0.0
	fn = 0.0
	# pdb.set_trace()
	max_ex = len(test_df)
	for i in range(max_ex):
		base_prompt = get_prompt(i, test_df, config.prompt_type)
		if config.indicator_type == 'pre':
			base_prompt = base_prompt + ' [correct]'
		full_response = ""
		corr_response = ""
		buffer_response = ""
		indi_flag = 0
		temps = [config.temperature, config.indi_temperature]
		qa = "\n".join(base_prompt.split("\n")[-2:])
		for j in range(config.max_calls_per_ex):
			regen_flag = 0
			start_time = time.time()
			# print("base prompt: ", base_prompt)
			# print()
			# print("temp: ", str(temps[indi_flag]))
			# print()
			response = openai.Completion.create(
				engine=config.model,
				prompt=base_prompt,
				max_tokens=config.max_tokens,
				temperature=temps[indi_flag],
				top_p=config.top_p,
				n=config.n,
				stop=stop_sequences,
				presence_penalty=config.presence_penalty,
				frequency_penalty=config.frequency_penalty,
				best_of=1
			)
			end_time = time.time()
			time_taken = end_time - start_time
			if config.sleep_btw == 'yes' and time_taken < config.time_per_request:
				time.sleep(config.time_per_request-time_taken)
			response = response["choices"][0]["text"].split("\n")[0].strip()
			# print("response: ", response)
			# print("-------------------------------")
			try:
				if response[-1] == ".":
					response = response[:-1]
			except:
				regen_flag = 1

			if not regen_flag:
				if config.indicator_type == 'post':
					if config.indi_temp:
						if "wrong" in response or "incorrect" in response or "correct" in response:
							full_response = full_response + " " + response + "]."
							if "wrong" in response or "incorrect" in response:
								if config.rep_ques:
									base_prompt = base_prompt + " " + response + "].\n" + qa
								else:
									base_prompt = base_prompt + " " + response + "]."
							else:
								base_prompt = base_prompt + " " + response + "]."
								corr_response = corr_response + " " + buffer_response + ". " + response + "]."
								if "answer" in buffer_response:
									break
							indi_flag = 0
						else:
							full_response = full_response + " " + response + "."
							base_prompt = base_prompt + " " + response + "."
							buffer_response = response
							indi_flag = 1
					else:
						full_response = full_response + " " + response + "."
						if "wrong" in response or "incorrect" in response:
							if config.rep_ques:
								base_prompt = base_prompt + " " + response + ".\n" + qa
							else:
								base_prompt = base_prompt + " " + response + "."
						else:
							base_prompt = base_prompt + " " + response + "."
							corr_response = corr_response + " " + response + "."
							if "answer" in response:
								break
				else:
					full_response = full_response + " " + response + "."
					base_prompt = base_prompt + " " + response + " [correct]"
					corr_response = corr_response + " " + response + "."
					if "answer" in response:
						break
		# pdb.set_trace()

		try:
			if corr_response[-1] == ".":
				corr_response = corr_response[:-1]
		except:
			corr_response = "0.179"
		corr_response = corr_response.replace(",", "")
		corr_response = corr_response.replace("$", "")
		corr_response = corr_response.replace("€", "")
		corr_response = corr_response.replace("%", "")
		num_ls = []
		for t in corr_response.split()[-7:]:
			try:
				num_ls.append(float(t))
			except ValueError:
				pass
		try:
			corr_response = num_ls[-1]
		except:
			corr_response = 0.179

		tot += 1
		disp_corr = 0
		if corr_response == test_df.loc[i]["Output"]:
			corr += 1
			disp_corr = 1

		with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
			f_out.write('---------------------------------------\n')
			f_out.write('Example: ' + str(i) + '\n')
			f_out.write('Source: ' + test_df.loc[i]["Input"] + '\n')
			f_out.write('Target: ' + str(test_df.loc[i]["Output"]) + '\n')
			f_out.write('Generated: ' + str(corr_response) + '\n')
			f_out.write('Result: ' + str(disp_corr) + '\n')
			# if config.check_pred == "yes":
			# 	f_out.write('Model Thinks: ' + str(model_check) + '\n')
			f_out.write('Full Response: ' + str(full_response) + '\n')
			# if config.check_pred == "yes":
			# 	f_out.write('Full Correctness: ' + str(full_correctness) + '\n')
			# 	if model_check == 0:
			# 		f_out.write('Critique: ' + str(critique) + '\n')
			f_out.write('\n')
			f_out.write('---------------------------------------\n')
			f_out.close()

		print("Completed {} / {}...".format(i+1, max_ex), end = '\r', flush = True)
	
	# pdb.set_trace()
	acc = corr/tot
	return acc, tp, fn, fp, tn


def run_evaluation_data():
	corr = 0.0
	tot = 0.0
	tp = 0.0
	tn = 0.0
	fp = 0.0
	fn = 0.0
	max_ex = len(test_df)
	for i in range(max_ex):
		# pdb.set_trace()
		# if i>0 and i%50 == 0 and config.sleep_btw=='yes':
		# 	time.sleep(60)
		start_time = time.time()
		response = openai.Completion.create(
			engine=config.model,
			prompt=get_prompt(i, test_df, config.prompt_type),
			max_tokens=config.max_tokens,
			temperature=config.temperature,
			top_p=config.top_p,
			n=config.n,
			stop=config.stop_seq,
			presence_penalty=config.presence_penalty,
			frequency_penalty=config.frequency_penalty,
			best_of=1
		)
		end_time = time.time()
		time_taken = end_time - start_time
		if config.sleep_btw == 'yes' and time_taken < config.time_per_request:
			time.sleep(config.time_per_request-time_taken)
		if config.eval_type == "normal":
			response = response["choices"][0]["text"].split("\n")[0].strip()
			full_response = response
		elif config.eval_type == "math":
			response = response["choices"][0]["text"]
			full_response = response
			try:
				if response[-1] == ".":
					response = response.split("\nQ")[0].strip()[:-1]
			except:
				response = "0.179"
			response = response.replace(",", "")
			response = response.replace("$", "")
			response = response.replace("€", "")
			response = response.replace("%", "")
			num_ls = []
			for t in response.split():
				try:
					num_ls.append(float(t))
				except ValueError:
					pass
			try:
				response = num_ls[-1]
			except:
				response = 0.179

		if config.check_pred == "yes":
			meta_data = {}
			meta_data["Q"] = test_df.loc[i]["Input"]
			meta_data["A"] = full_response

			# correctness = openai.Completion.create(
			# 	engine=config.model,
			# 	prompt=get_prompt(i, test_df, "math_prediction", meta_data),
			# 	max_tokens=config.max_tokens,
			# 	temperature=config.temperature,
			# 	top_p=config.top_p,
			# 	n=config.n,
			# 	stop=config.stop_seq,
			# 	presence_penalty=config.presence_penalty,
			# 	frequency_penalty=config.frequency_penalty,
			# 	best_of=1
			# )
			# correctness = correctness["choices"][0]["text"].split("\n")[0].strip()
			# full_correctness = correctness
			# if correctness[-1] == ".":
			# 	correctness = correctness[:-1]
			# correctness = correctness.split()[-1]
			# if correctness == "incorrect":
			# 	model_check = 0
			# 	critique = openai.Completion.create(
			# 		engine=config.model,
			# 		prompt=get_prompt(i, test_df, "math_critique", meta_data),
			# 		max_tokens=config.max_tokens,
			# 		temperature=config.temperature,
			# 		top_p=config.top_p,
			# 		n=config.n,
			# 		stop=config.stop_seq,
			# 		presence_penalty=config.presence_penalty,
			# 		frequency_penalty=config.frequency_penalty,
			# 		best_of=1
			# 	)
			# 	critique = critique["choices"][0]["text"].split("\n")[0].strip()
			# else:
			# 	model_check = 1
			critique = openai.Completion.create(
				engine=config.model,
				prompt=get_prompt(i, test_df, "math_prediction_critique", meta_data),
				max_tokens=config.max_tokens,
				temperature=config.temperature,
				top_p=config.top_p,
				n=config.n,
				stop=config.stop_seq,
				presence_penalty=config.presence_penalty,
				frequency_penalty=config.frequency_penalty,
				best_of=1
			)
			critique = critique["choices"][0]["text"].split("\n")[0].strip()
			full_correctness = critique.split(".")[0].strip()
			correctness = critique.split(".")[0].strip().split()[-1]
			if correctness == "incorrect":
				model_check = 0
			else:
				model_check = 1

		tot += 1
		disp_corr = 0
		if response == test_df.loc[i]["Output"]:
			corr += 1
			disp_corr = 1
			if config.check_pred == "yes":
				if model_check == 1:
					tp += 1
				else:
					fn += 1
		else:
			if config.check_pred == "yes":
				if model_check == 1:
					fp += 1
				else:
					tn += 1

		with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
			f_out.write('---------------------------------------\n')
			f_out.write('Example: ' + str(i) + '\n')
			f_out.write('Source: ' + test_df.loc[i]["Input"] + '\n')
			f_out.write('Target: ' + str(test_df.loc[i]["Output"]) + '\n')
			f_out.write('Generated: ' + str(response) + '\n')
			f_out.write('Result: ' + str(disp_corr) + '\n')
			if config.check_pred == "yes":
				f_out.write('Model Thinks: ' + str(model_check) + '\n')
			f_out.write('Full Response: ' + str(full_response) + '\n')
			if config.check_pred == "yes":
				f_out.write('Full Correctness: ' + str(full_correctness) + '\n')
				if model_check == 0:
					f_out.write('Critique: ' + str(critique) + '\n')
			f_out.write('\n')
			f_out.write('---------------------------------------\n')
			f_out.close()

		print("Completed {} / {}...".format(i+1, max_ex), end = '\r', flush = True)
	
	# pdb.set_trace()
	acc = corr/tot
	return acc, tp, fn, fp, tn

def run_evaluation_permute():
	corr = 0.0
	tot = 0.0
	tp = 0.0
	tn = 0.0
	fp = 0.0
	fn = 0.0
	# pdb.set_trace()

	base_prompt = get_prompt(0, test_df, config.prompt_type)
	permute_data = permute_prompts(base_prompt, 1)

	max_ex = len(permute_data)

	for i in range(max_ex):
		curr_combi = permute_data[i]
		for j in range(len(curr_combi[1])):
			quest = curr_combi[1][j].split("\n")[0]
			true_ans = curr_combi[1][j].split("\n")[1]
			curr_prompt = "\n".join(curr_combi[0]) + "\n" + quest + "\nA:"
			start_time = time.time()
			response = openai.Completion.create(
				engine=config.model,
				prompt=curr_prompt,
				max_tokens=config.max_tokens,
				temperature=config.temperature,
				top_p=config.top_p,
				n=config.n,
				stop=config.stop_seq,
				presence_penalty=config.presence_penalty,
				frequency_penalty=config.frequency_penalty,
				best_of=1
			)
			end_time = time.time()
			time_taken = end_time - start_time
			if config.sleep_btw == 'yes' and time_taken < config.time_per_request:
				time.sleep(config.time_per_request-time_taken)
			
			response = response["choices"][0]["text"].split("\n")[0].strip()
			ans = true_ans.strip()
			full_response = response
			try:
				if response[-1] == ".":
					response = response[:-1]
				if ans[-1] == ".":
					ans = ans[:-1]
			except:
				response = "0.179"
				ans = "0.189"
			response = response.replace(",", "")
			response = response.replace("$", "")
			response = response.replace("%", "")
			ans = ans.replace(",", "")
			ans = ans.replace("$", "")
			ans = ans.replace("%", "")
			num_ls = []
			for t in response.split():
				try:
					num_ls.append(float(t))
				except ValueError:
					pass
			try:
				response = num_ls[-1]
			except:
				response = 0.179

			num_ls = []
			for t in ans.split():
				try:
					num_ls.append(float(t))
				except ValueError:
					pass
			try:
				ans = num_ls[-1]
			except:
				ans = 0.189

			tot += 1
			disp_corr = 0
			if response == ans:
				corr += 1
				disp_corr = 1

			with open(config.outputs_path + '/outputs.txt', 'a') as f_out:
				f_out.write('---------------------------------------\n')
				f_out.write('Example: ' + str(i) + "-" + str(j) + '\n')
				f_out.write('Prompt: ' + curr_prompt + '\n')
				f_out.write('Source: ' + quest + '\n')
				f_out.write('Target: ' + str(ans) + '\n')
				f_out.write('Generated: ' + str(response) + '\n')
				f_out.write('Result: ' + str(disp_corr) + '\n')
				f_out.write('Full Response: ' + str(full_response) + '\n')
				f_out.write('\n')
				f_out.write('---------------------------------------\n')
				f_out.close()
			print("Completed {} / {}...".format(j+1, len(curr_combi[1])), end = '\r', flush = True)

		print("Completed {} / {}...".format(i+1, max_ex), end = '\r', flush = True)
	
	# pdb.set_trace()
	acc = corr/tot
	return acc, tp, fn, fp, tn


# acc, tp, fn, fp, tn = run_evaluation_data()
# acc, tp, fn, fp, tn = run_evaluation_permute()
# acc, tp, fn, fp, tn = run_evaluation_with_mistakes()
# acc = run_evaluation_with_mistakes_multi_sample()
# pdb.set_trace()
if config.exp_type == "multi_sample":
	code_flag = 1
	while (code_flag):
		try:
			acc = run_evaluation_with_mistakes_multi_sample(example)
			code_flag = 0
		except:
			pass
else:
	acc, tp, fn, fp, tn = run_evaluation_data()
	# acc, tp, fn, fp, tn = run_evaluation_permute()
	# acc, tp, fn, fp, tn = run_evaluation_with_mistakes()


store_results(config, acc)
print()
print("Accuracy: ", str(acc))
if config.check_pred == "yes":
	print("True Positives: ", tp)
	print("False Negatives: ", fn)
	print("False Positives: ", fp)
	print("True Negatives: ", tn)