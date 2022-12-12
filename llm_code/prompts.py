from email.mime import base
from itertools import combinations

def get_prompt(i, df, prompt_type, meta_data = {"Q": ""}):
	if prompt_type == "math_cot_default":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: There are 15 trees originally. Then there were 21 trees after some more were planted. So there must have been 21 - 15 = 6. The answer is 6." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are originally 3 cars. 2 more cars arrive. 3 + 2 = 5. The answer is 5." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Originally, Leah had 32 chocolates. Her sister had 42. So in total they had 32 + 42 = 74. After eating 35, they had 74 - 35 = 39. The answer is 39." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason started with 20 lollipops. Then he had 12 after giving some to Denny. So he gave Denny 20 - 12 = 8. The answer is 8." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: Shawn started with 5 toys. If he got 2 toys each from his mom and dad, then that is 4 more toys. 5 + 4 = 9. The answer is 9." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were originally 9 computers. For each of 4 days, 5 more computers were added. So 5 * 4 = 20 computers were added. 9 + 20 is 29. The answer is 29." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael started with 58 golf balls. After losing 23 on tuesday, he had 58 - 23 = 35. After losing 2 more, he had 35 - 2 = 33 golf balls. The answer is 33." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia had 23 dollars. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. So she has 23 - 15 dollars left. 23 - 15 is 8. The answer is 8." + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math_cot_default_mistake_pre_indicators":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: [wrong] The grove workers planted 15 + 21 = 36 trees today. [" + \
					"\nQ: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: [correct] There are 15 trees originally. [correct] Then there were 21 trees after some more were planted. [correct] So there must have been 21 - 15 = 6. [correct] The answer is 6. [" + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: [correct] There are originally 3 cars. [correct] 2 more cars arrive. [correct] 3 + 2 = 5. [correct] The answer is 5. [" + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: [correct] Leah had 32 chocolates and her sister had 42. [correct] They ate 35 chocolates. [wrong] So they have 32 - 35 = -3 chocolates. [" + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: [correct] Leah had 32 chocolates and her sister had 42. [correct] They ate 35. [wrong] So they have 32 - 35 = -3 and 42 - 35 = 7. [" + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: [correct] Leah had 32 chocolates and her sister had 42. [correct] They ate 35 chocolates. [wrong] 32 + 42 - 35 = 49. [" + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: [correct] Originally, Leah had 32 chocolates. [correct] Her sister had 42. [correct] So in total they had 32 + 42 = 74. [correct] After eating 35, they had 74 - 35 = 39. [correct] The answer is 39. [" + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: [correct] Jason started with 20 lollipops. [correct] Then he had 12 after giving some to Denny. [correct] So he gave Denny 20 - 12 = 8. [correct] The answer is 8. [" + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: [correct] Shawn started with 5 toys. [correct] If he got 2 toys each from his mom and dad, then that is 4 more toys. [correct] 5 + 4 = 9. [correct] The answer is 9. [" + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: [wrong] On monday, there were 9 computers. [" + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: [correct] There were 9 computers in the server room. [correct] 5 more were installed each day from Monday to Thursday. [correct] So that is 5 + 5 + 5 + 5 = 20. [wrong] The answer is 20. [" + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: [correct] There were originally 9 computers. [correct] For each of 4 days, 5 more computers were added. [correct] So 5 * 4 = 20 computers were added. [correct] 9 + 20 is 29. [correct] The answer is 29. [" + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: [correct] Michael started with 58 golf balls. [correct] After losing 23 on tuesday, he had 58 - 23 = 35. [correct] After losing 2 more, he had 35 - 2 = 33 golf balls. [correct] The answer is 33. [" + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: [wrong] Olivia has $2 left. [" + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: [correct] Olivia had 23 dollars. [correct] 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. [correct] So she has 23 - 15 dollars left. [correct] 23 - 15 is 8. [correct] The answer is 8. [" + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math_cot_default_mistake_post_indicators":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: The grove workers planted 15 + 21 = 36 trees today [wrong]." + \
					"\nQ: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: There are 15 trees originally [correct]. Then there were 21 trees after some more were planted [correct]. So there must have been 21 - 15 = 6 [correct]. The answer is 6 [correct]." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are originally 3 cars [correct]. 2 more cars arrive [correct]. 3 + 2 = 5 [correct]. The answer is 5 [correct]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42 [correct]. They ate 35 chocolates [correct]. So they have 32 - 35 = -3 chocolates [wrong]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42 [correct]. They ate 35 [correct]. So they have 32 - 35 = -3 and 42 - 35 = 7 [wrong]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42 [correct]. They ate 35 chocolates [correct]. 32 + 42 - 35 = 49 [wrong]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Originally, Leah had 32 chocolates [correct]. Her sister had 42 [correct]. So in total they had 32 + 42 = 74 [correct]. After eating 35, they had 74 - 35 = 39 [correct]. The answer is 39 [correct]." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason started with 20 lollipops [correct]. Then he had 12 after giving some to Denny [correct]. So he gave Denny 20 - 12 = 8 [correct]. The answer is 8 [correct]." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: Shawn started with 5 toys [correct]. If he got 2 toys each from his mom and dad, then that is 4 more toys [correct]. 5 + 4 = 9 [correct]. The answer is 9 [correct]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: On monday, there were 9 computers [wrong]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were 9 computers in the server room [correct]. 5 more were installed each day from Monday to Thursday [correct]. So that is 5 + 5 + 5 + 5 = 20 [correct]. The answer is 20 [wrong]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were originally 9 computers [correct]. For each of 4 days, 5 more computers were added [correct]. So 5 * 4 = 20 computers were added [correct]. 9 + 20 is 29 [correct]. The answer is 29 [correct]." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael started with 58 golf balls [correct]. After losing 23 on tuesday, he had 58 - 23 = 35 [correct]. After losing 2 more, he had 35 - 2 = 33 golf balls [correct]. The answer is 33 [correct]." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia has $2 left [wrong]." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia had 23 dollars [correct]. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars [correct]. So she has 23 - 15 dollars left [correct]. 23 - 15 is 8 [correct]. The answer is 8 [correct]." + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math_cot_default_mistake_post_indicators_2":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: The grove workers planted 15 + 21 = 36 trees today. [This is incorrect]." + \
					"\nQ: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: There are 15 trees originally. [This is correct]. Then there were 21 trees after some more were planted. [This is correct]. So there must have been 21 - 15 = 6. [This is correct]. The answer is 6. [This is correct]." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are originally 3 cars. [This is correct]. 2 more cars arrive. [This is correct]. 3 + 2 = 5. [This is correct]. The answer is 5. [This is correct]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42. [This is correct]. They ate 35 chocolates. [This is correct]. So they have 32 - 35 = -3 chocolates. [This is incorrect]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42. [This is correct]. They ate 35. [This is correct]. So they have 32 - 35 = -3 and 42 - 35 = 7. [This is incorrect]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42. [This is correct]. They ate 35 chocolates. [This is correct]. 32 + 42 - 35 = 49. [This is incorrect]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Originally, Leah had 32 chocolates. [This is correct]. Her sister had 42. [This is correct]. So in total they had 32 + 42 = 74. [This is correct]. After eating 35, they had 74 - 35 = 39. [This is correct]. The answer is 39. [This is correct]." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason started with 20 lollipops. [This is correct]. Then he had 12 after giving some to Denny. [This is correct]. So he gave Denny 20 - 12 = 8. [This is correct]. The answer is 8. [This is correct]." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: Shawn started with 5 toys. [This is correct]. If he got 2 toys each from his mom and dad, then that is 4 more toys. [This is correct]. 5 + 4 = 9. [This is correct]. The answer is 9. [This is correct]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: On monday, there were 9 computers. [This is incorrect]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were 9 computers in the server room. [This is correct]. 5 more were installed each day from Monday to Thursday. [This is correct]. So that is 5 + 5 + 5 + 5 = 20. [This is correct]. The answer is 20. [This is incorrect]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were originally 9 computers. [This is correct]. For each of 4 days, 5 more computers were added. [This is correct]. So 5 * 4 = 20 computers were added. [This is correct]. 9 + 20 is 29. [This is correct]. The answer is 29. [This is correct]." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael started with 58 golf balls. [This is correct]. After losing 23 on tuesday, he had 58 - 23 = 35. [This is correct]. After losing 2 more, he had 35 - 2 = 33 golf balls. [This is correct]. The answer is 33. [This is correct]." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia has $2 left. [This is incorrect]." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia had 23 dollars. [This is correct]. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. [This is correct]. So she has 23 - 15 dollars left. [This is correct]. 23 - 15 is 8. [This is correct]. The answer is 8. [This is correct]." + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math_cot_default_mistake_post_indicators_3":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: The grove workers planted 15 + 21 = 36 trees today. [This is incorrect]." + \
					"\nQ: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: The grove workers planted 15 + 21 = 36 trees today. [This is incorrect]. There are 15 trees originally. [This is correct]. Then there were 21 trees after some more were planted. [This is correct]. So there must have been 21 - 15 = 6. [This is correct]. The answer is 6. [This is correct]." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are originally 3 cars. [This is correct]. 2 more cars arrive. [This is correct]. 3 + 2 = 5. [This is correct]. The answer is 5. [This is correct]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and her sister had 42. [This is correct]. They ate 35 chocolates. [This is correct]. So they have 32 - 35 = -3 chocolates. [This is incorrect]. So they have 32 - 35 = -3 and 42 - 35 = 7. [This is incorrect]. 32 + 42 - 35 = 49. [This is incorrect]. So they have 74 - 35 = 39. [This is correct].  The answer is 39. [This is correct]." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Originally, Leah had 32 chocolates. [This is correct]. Her sister had 42. [This is correct]. So in total they had 32 + 42 = 74. [This is correct]. After eating 35, they had 74 - 35 = 39. [This is correct]. The answer is 39. [This is correct]." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason started with 20 lollipops. [This is correct]. Then he had 12 after giving some to Denny. [This is correct]. So he gave Denny 20 - 12 = 8. [This is correct]. The answer is 8. [This is correct]." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: Shawn started with 5 toys. [This is correct]. If he got 2 toys each from his mom and dad, then that is 4 more toys. [This is correct]. 5 + 4 = 9. [This is correct]. The answer is 9. [This is correct]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: On monday, there were 9 computers. [This is incorrect]. Initially there were 9 computers. [This is correct]. 5 more were installed each day from Monday to Thursday. [This is correct]. So that is 5 + 5 + 5 + 5 = 20. [This is correct]. The answer is 20. [This is incorrect]. So we have a total of 9 + 20 = 29 computers. [This is correct]. The answer is 29. [This is correct]." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There were originally 9 computers. [This is correct]. For each of 4 days, 5 more computers were added. [This is correct]. So 5 * 4 = 20 computers were added. [This is correct]. 9 + 20 is 29. [This is correct]. The answer is 29. [This is correct]." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael started with 58 golf balls. [This is correct]. After losing 23 on tuesday, he had 58 - 23 = 35. [This is correct]. After losing 2 more, he had 35 - 2 = 33 golf balls. [This is correct]. The answer is 33. [This is correct]." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: Olivia has $2 left. [This is incorrect]. Olivia had 23 dollars. [This is correct]. 5 bagels for 3 dollars each will be 5 x 3 = 15 dollars. [This is correct]. So she has 23 - 15 dollars left. [This is correct]. 23 - 15 is 8. [This is correct]. The answer is 8. [This is correct]." + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 6 trees. The answer is 6." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74 chocolates. 35 have been eaten. So in total they still have 74 - 35 = 39 chocolates. The answer is 39." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. Then he got 2 more from dad, so in total he has 7 + 2 = 9 toys. The answer is 9." + \
					"\nQ: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There are 4 days from monday to thursday. 5 computers were added each day. That means in total 4 * 5 = 20 computers were added. There were 9 computers in the beginning, so now there are 9 + 20 = 29 computers. The answer is 29." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33." + \
					"\nQ: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: She bought 5 bagels for $3 each. This means she spent 5 * $3 = $15 on the bagels. She had $23 in beginning, so now she has $23 - $15 = $8. The answer is 8." + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
	elif prompt_type == "math_prediction":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 8 trees. The answer is 8." + \
					"\nP: The answer is incorrect." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5." + \
					"\nP: The answer is correct." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74 chocolates. 35 have been eaten. So in total they still have 74 - 32 = 42 chocolates. The answer is 42." + \
					"\nP: The answer is incorrect." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8." + \
					"\nP: The answer is correct." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. The answer is 7." + \
					"\nP: The answer is incorrect." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33." + \
					"\nP: The answer is correct." + \
					"\nQ: Olivia has $25. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: She bought 5 bagels using $25. This means she spent $25 / 5 = $5 on each bagel. So now she has $5 - $3 = $2. The answer is 2." + \
					"\nP: The answer is incorrect." + \
					"\nQ: Janet has 4 bags containing 7 marbles each. If she gives 12 marbles to Jill, how many marbles does she have left?" + \
					"\nA: Janet has 4 bags with 7 marbles in each bag. So she has 4 * 7 = 28 marbles. She gave 12 marbles to Jill. So she has 28 - 12 = 16 marbles left. The answer is 16." + \
					"\nP: The answer is correct." + \
					"\nQ: Bill had 39 chocolates. Jack took three chocolates from Bill. If Bill needs to distribute the remaining chocolates equally into 3 boxes, how many chocolates does he need to put in each box?" + \
					"\nA: Bill had 39 chocolates initially and Jack took three of them. This means he had 39 - 3 = 36 chocolates remaining. To distribute these chocolates into 3 boxes equally, he needs to put 36 / 3 = 12 chocolates in each box. The answer is 12." + \
					"\nP: The answer is correct." + \
					"\nQ: " + meta_data["Q"] + "\nA: " + meta_data["A"] + "\nP:"
					# "\nQ: There were nine computers in the server room. Seven more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					# "\nA: There are 4 days from monday to thursday. We need to add the number of days to the number of computers. That means in total 4 + 7 = 11 computers were added. There were 9 computers in the beginning, so now there are 9 + 11 = 20 computers. The answer is 20." + \
					# "\nP: The answer is incorrect." + \
	elif prompt_type == "math_critique":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 8 trees. The answer is 8." + \
					"\nC: There is a calculation mistake in the answer. Instead of 21 - 15 = 8, the correct equation is 21 - 15 = 6." + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74 chocolates. 35 have been eaten. So in total they still have 74 - 32 = 42 chocolates. The answer is 42." + \
					"\nC: There is a number mapping mistake in the answer. Instead of 32 in the equation 74 - 32 = 42, the number 35 should be used. So, the equation should be 74 - 35 = 39." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops and later he has 12 more lollipops. So the number of lollipops is 20 + 12 = 32. The answer is 32." + \
					"\nC: The answer applies the incorrect operation. To find the number of lollipops Jason gave to Denny, we need to subtract rather than add. So the correct equation is 20 - 12 = 8." + \
                    "\nQ: There were nine computers in the server room. Seven more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There are 4 days from monday to thursday. We need to add the number of days to the number of computers. That means in total 4 + 7 = 11 computers were added. There were 9 computers in the beginning, so now there are 9 + 11 = 20 computers. The answer is 20." + \
					"\nC: The reasoning of the answer is flawed. We need to multiply the number of days to the number of computers installed each day. So, instead of 4 + 7 = 11, the correct equation is 4 * 7 = 28." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. The answer is 7." + \
					"\nC: The answer misses one reasoning step. Apart from getting 2 toys from mom, the boy also got 2 toys from dad. So, the equation 7 + 2 = 9 should be included." + \
					"\nQ: Olivia has $25. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: She bought 5 bagels using $25. This means she spent $25 / 5 = $5 on each bagel. So now she has $5 - $3 = $2. The answer is 2." + \
					"\nC: There is a flaw in the reasoning. She bought 5 bagels for $3 each. So she spent 5 * $3 = $15 on the bagels. This amount needs to be subtracted from the money she initially had to obtain the correct answer." + \
					"\nQ: Janet has 4 bags containing 16 marbles each. If she gives 2 marbles to Jill, how many marbles does she have left?" + \
					"\nA: Janet has 4 bags with 16 marbles in each bag. So she has 16 / 4 = 4 marbles. She gave 2 marbles to Jill. So she has 4 - 2 = 2 marbles left. The answer is 2." + \
					"\nC: The answer has flawed reasoning. Since she has 4 bags containing 16 marbles each, she has a total of 4 * 16 = 64 marbles before she gave 2 marbles to Jill." + \
					"\nQ: Bill had 39 chocolates. Jack took three chocolates from Bill. If Bill needs to distribute the remaining chocolates equally into 3 boxes, how many chocolates does he need to put in each box?" + \
					"\nA: Bill needs to distribute the chocolates into three boxes. This means he had 39 / 3 = 13 chocolates in each box. Since Jack took three chocolates, there are 13 - 3 = 10 chocolates. The answer is 10." + \
					"\nC: The answer has a wrong sequence of reasoning steps. First Jack took three chocolates from Bill resulting in a total of 39 - 3 = 36 chocolates. These 36 chocolates now need to be distributed equally into three boxes." + \
					"\nQ: " + meta_data["Q"] + "\nA: " + meta_data["A"] + "\nC:"
	elif prompt_type == "math_critique_together":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 8 trees. The answer is 8." + \
					"\nC: The answer is incorrect. There is a calculation mistake in the answer. Instead of 21 - 15 = 8, the correct equation is 21 - 15 = 6. The answer is 6. [End]" + \
					"\nQ: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 6 trees. The answer is 6." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: On Monday, Janet bought a dozen chocolates. On Tuesday, she bought twice the number of chocolates she bought on Monday. On Wednesday, she bought half the number of chocolates she bought on Monday. How many chocolates did she buy over the course of the three days?" + \
					"\nA: Janet bought a dozen chocolates on Monday. She bought twice that number of chocolates on Tuesday. So she bought 2 * 12 = 24 chocolates on Tuesday. She bought half the number of chocolates on Wednesday. So she bought 0.5 * 24 = 12 chocolates on Wednesday. The total number of chocolates she bought is 24 + 12 = 36. The answer is 36." + \
					"\nC: The answer is incorrect. Janet bought a dozen chocolates, meaning she bought 12 chocolates on Monday. She bought twice that number of chocolates on Tuesday. So she bought 2 * 12 = 24 chocolates on Tuesday. On Wednesday, she bought half of the number of chocolates she bought on Monday. So she bought 0.5 * 12 = 6 chocolates on Wednesday. Now the number of chocolates she bought on all three days need to be added up. So she bought 12 + 24 + 6 = 42 chocolates. The answer is 42. [End]" + \
					"\nQ: There were nine computers in the server room. Seven more computers were installed each day, from monday to thursday. How many computers are now in the server room?" + \
					"\nA: There are 4 days from monday to thursday. We need to add the number of days to the number of computers. That means in total 4 + 7 = 11 computers were added. There were 9 computers in the beginning, so now there are 9 + 11 = 20 computers. The answer is 20." + \
					"\nC: The answer is incorrect. The reasoning of the answer is flawed. We need to multiply the number of days to the number of computers installed each day. So, instead of 4 + 7 = 11, the correct equation is 4 * 7 = 28. There were 9 computers in the beginning, so now there are 9 + 28 = 37 computers. [End]" + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. The answer is 7." + \
					"\nC: The answer is incorrect. The answer misses one reasoning step. Apart from getting 2 toys from mom, the boy also got 2 toys from dad. So, the equation 7 + 2 = 9 should be included. The answer is 9. [End]" + \
					"\nQ: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?" + \
					"\nA: Leah had 32 chocolates and Leah’s sister had 42. That means there were originally 32 + 42 = 74 chocolates. 35 have been eaten. So in total they still have 74 - 32 = 42 chocolates. The answer is 42." + \
					"\nC: The answer is incorrect. There is a number mapping mistake in the answer. Instead of 32 in the equation 74 - 32 = 42, the number 35 should be used. So, the equation should be 74 - 35 = 39. The answer is 39. [End]" + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops and later he has 12 more lollipops. So the number of lollipops is 20 + 12 = 32. The answer is 32." + \
					"\nC: The answer is incorrect. The answer applies the incorrect operation. To find the number of lollipops Jason gave to Denny, we need to subtract rather than add. So the correct equation is 20 - 12 = 8. The answer is 8. [End]" + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: Olivia has $25. She bought five bagels for $3 each. How much money does she have left?" + \
					"\nA: She bought 5 bagels using $25. This means she spent $25 / 5 = $5 on each bagel. So now she has $5 - $3 = $2. The answer is 2." + \
					"\nC: The answer is incorrect. There is a flaw in the reasoning. She bought 5 bagels for $3 each. So she spent 5 * $3 = $15 on the bagels. This amount needs to be subtracted from the money she initially had to obtain the correct answer. So now she has $25 - $15 = $10. The answer is 10. [End]" + \
					"\nQ: The price of a balloon is $3. This price increases every 3 days by 10% of the original price. How much would the balloon cost in 9 days?" + \
					"\nA: The price of the balloon increases by 10% every 3 days. This means that the price increases by 10% * 3 = 30% every day. After 9 days, the price will increase by 9 * 30% = 270%. The original price is $3, so now the price is $3 * (1 + 270%) = $3 * (1 + 2.7) = $3 * 3.7 = $11.1. The answer is 11.1." + \
					"\nC: The answer is incorrect. The original price of the balloon is $3. This price increases by 10% every 3 days. This means that the price increases by $3 * 10/100 = $0.3 every 3 days. So the price increases by $0.3/3 = $0.1 every day. After 9 days, the price is increased by 9 * $0.1 = $0.9. So the final price of the balloon is $3 + $0.9 = $3.9. The answer is 3.9. [End]" + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: Janet has 4 bags containing 16 marbles each. If she gives 2 marbles to Jill, how many marbles does she have left?" + \
					"\nA: Janet has 4 bags with 16 marbles in each bag. So she has 16 / 4 = 4 marbles. She gave 2 marbles to Jill. So she has 4 - 2 = 2 marbles left. The answer is 2." + \
					"\nC: The answer is incorrect. The answer has flawed reasoning. Since she has 4 bags containing 16 marbles each, she has a total of 4 * 16 = 64 marbles before she gave 2 marbles to Jill. So she has 64 - 2 = 62 marbles left. The answer is 62. [End]" + \
					"\nQ: Janet has 4 bags containing 7 marbles each. If she gives 12 marbles to Jill, how many marbles does she have left?" + \
					"\nA: Janet has 4 bags with 7 marbles in each bag. So she has 4 * 7 = 28 marbles. She gave 12 marbles to Jill. So she has 28 - 12 = 16 marbles left. The answer is 16." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. How many hours does will it take him to run up 12 hills and cut 18 trees?" + \
					"\nA: Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. So it takes him 10/60 = 1/6 hours to run up a hill and 5/60 = 1/12 hours to cut a tree. He needs to run up 12 hills and cut 18 trees. So, it will take him 12 * 1/6 + 18 * 1/12 = 1 + 1/3 = 4/3 hours. The answer is 4/3." + \
					"\nC: The answer is incorrect. Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. So it takes him 10/60 = 1/6 hours to run up a hill and 5/60 = 1/12 hours to cut a tree. He needs to run up 12 hills and cut 18 trees. So, it will take him 12 * 1/6 + 18 * 1/12 = 2 + 3/2 = 2 + 1.5 = 3.5 hours. The answer is 3.5. [End]" + \
					"\nQ: Harry is two feet taller than John, who is three feet shorter than Mary. Mary is four feet taller than Jason. Jason is twice as tall as Gary. If Gary is 3 feet tall, how tall is Harry?" + \
					"\nA: Harry is two feet taller than John and John is three feet shorter than Mary. This means that Harry is 2 + 3 = 5 feet taller than Mary. Mary is four feet taller than Jason. This means that Harry is 5 + 4 = 9 feet taller than Jason. Jason is twice as tall as Gary. This means that Harry is 2 * 9 = 18 feet taller than Gary. Gary is 3 feet tall. This means that Harry is 18 + 3 = 21 feet tall. The answer is 21." + \
					"\nC: The answer is incorrect. Gary is 3 feet tall and Jason is twice as tall as Gary. This means that Jason is 2 * 3 = 6 feet tall. Mary is 4 feet taller than Jason, so Mary is 6 + 4 = 10 feet tall. John is 3 feet shorter than Mary, so John is 10 - 3 = 7 feet tall. Harry is 2 feet taller than John. This means that Harry is 2 + 7 = 9 feet tall. The answer is 9. [End]" + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: Bill had 39 chocolates. Jack took three chocolates from Bill. If Bill needs to distribute the remaining chocolates equally into 3 boxes, how many chocolates does he need to put in each box?" + \
					"\nA: Bill needs to distribute the chocolates into three boxes. This means he had 39 / 3 = 13 chocolates in each box. Since Jack took three chocolates, there are 13 - 3 = 10 chocolates. The answer is 10." + \
					"\nC: The answer is incorrect. The answer has a wrong sequence of reasoning steps. First Jack took three chocolates from Bill resulting in a total of 39 - 3 = 36 chocolates. These 36 chocolates now need to be distributed equally into three boxes. This means he had 36 / 3 = 12 chocolates in each box. The answer is 12. [End]" + \
					"\nQ: Bill had 39 marbles. Jack took five marbles from Bill. If Bill needs to distribute the remaining marbles equally into 2 sets, how many marbles does he need to put in each set?" + \
					"\nA: Bill had 39 marbles initially and Jack took five of them. This means he had 39 - 5 = 34 marbles remaining. To distribute these marbles into 2 sets equally, he needs to put 34 / 2 = 17 marbles in each set. The answer is 17." + \
					"\nC: The answer is correct. [End]" + \
					"\nQ: " + df.loc[i]["Input"] + "\nA:"
					# "\nQ: A box can contain 5 envelopes and each envelope can carry 10 papers. If Jack delivers 50 boxes every day, how many papers get delivered every week?" + \
					# "\nA: A box has 5 envelopes and an envelope has 10 papers. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day." + \
					# "\nC: The answer is incorrect. A box has 5 envelopes and each envelope has 10 papers. This means that each box has 5 * 10 = 50 papers. Jack delivers 50 boxes every day, so he delivers 50 * 50 = 2,500 papers every day. This means that every week, he delivers 7 * 2,500 = 17,500 papers. The answer is 17,500." + \
					# "\nQ: Sam had 39 chocolates. Carl took three chocolates from Sam. If Sam needs to distribute the remaining chocolates equally into 3 boxes, how many chocolates does he need to put in each box?" + \
					# "\nA: Sam needs to distribute the chocolates into three boxes. This means he had 39 / 3 = 13 chocolates in each box. Since Carl took three chocolates, there are 13 - 3 = 10 chocolates. The answer is 10." + \
					# "\nC: The answer is incorrect. Carl took three chocolates from Sam, so Sam has 39 - 3 = 36 chocolates. Sam needs to distribute the chocolates equally into three boxes. So, he needs to put 36 / 3 = 12 chocolates in each box. The answer is 12." + \
	elif prompt_type == "math_prediction_critique":
		prompt = "Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?" + \
					"\nA: We start with 15 trees. Later we have 21 trees. The difference must be the number of trees they planted. So, they must have planted 21 - 15 = 6 trees. The answer is 6." + \
					"\nC: The answer is correct." + \
					"\nQ: On Monday, Janet bought a dozen chocolates. On Tuesday, she bought twice the number of chocolates she bought on Monday. On Wednesday, she bought half the number of chocolates she bought on Monday. How many chocolates did she buy over the course of the three days?" + \
					"\nA: Janet bought a dozen chocolates on Monday. She bought twice that number of chocolates on Tuesday. So she bought 2 * 12 = 24 chocolates on Tuesday. She bought half the number of chocolates on Wednesday. So she bought 0.5 * 24 = 12 chocolates on Wednesday. The total number of chocolates she bought is 24 + 12 = 36. The answer is 36." + \
					"\nC: The answer is incorrect. Janet bought a dozen chocolates, meaning she bought 12 chocolates on Monday. She bought twice that number of chocolates on Tuesday. So she bought 2 * 12 = 24 chocolates on Tuesday. On Wednesday, she bought half of the number of chocolates she bought on Monday. So she bought 0.5 * 12 = 6 chocolates on Wednesday. Now the number of chocolates she bought on all three days need to be added up. So she bought 12 + 24 + 6 = 42 chocolates. The answer is 42." + \
					"\nQ: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?" + \
					"\nA: He has 5 toys. He got 2 from mom, so after that he has 5 + 2 = 7 toys. The answer is 7." + \
					"\nC: The answer is incorrect. Shawn has 5 toys and he got 2 each from his mom and dad. This means he has 5 + 2 + 2 = 9 toys. The answer is 9." + \
					"\nQ: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?" + \
					"\nA: Jason had 20 lollipops. Since he only has 12 now, he must have given the rest to Denny. The number of lollipops he has given to Denny must have been 20 - 12 = 8 lollipops. The answer is 8." + \
					"\nC: The answer is correct." + \
					"\nQ: The price of a balloon is $3. This price increases every 3 days by 10% of the original price. How much would the balloon cost in 9 days?" + \
					"\nA: The price of the balloon increases by 10% every 3 days. This means that the price increases by 10% * 3 = 30% every day. After 9 days, the price will increase by 9 * 30% = 270%. The original price is $3, so now the price is $3 * (1 + 270%) = $3 * (1 + 2.7) = $3 * 3.7 = $11.1. The answer is 11.1." + \
					"\nC: The answer is incorrect. The original price of the balloon is $3. This price increases by 10% every 3 days. This means that the price increases by $3 * 10/100 = $0.3 every 3 days. So the price increases by $0.3/3 = $0.1 every day. After 9 days, the price is increased by 9 * $0.1 = $0.9. So the final price of the balloon is $3 + $0.9 = $3.9. The answer is 3.9." + \
					"\nQ: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?" + \
					"\nA: Michael initially had 58 balls. He lost 23 on Tuesday, so after that he has 58 - 23 = 35 balls. On Wednesday he lost 2 more so now he has 35 - 2 = 33 balls. The answer is 33." + \
					"\nC: The answer is correct." + \
					"\nQ: Janet has 4 bags containing 7 marbles each. If she gives 12 marbles to Jill, how many marbles does she have left?" + \
					"\nA: Janet has 4 bags with 7 marbles in each bag. So she has 4 * 7 = 28 marbles. She gave 12 marbles to Jill. So she has 28 - 12 = 16 marbles left. The answer is 16." + \
					"\nC: The answer is correct." + \
					"\nQ: Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. How many hours does will it take him to run up 12 hills and cut 18 trees?" + \
					"\nA: Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. So it takes him 10/60 = 1/6 hours to run up a hill and 5/60 = 1/12 hours to cut a tree. He needs to run up 12 hills and cut 18 trees. So, it will take him 12 * 1/6 + 18 * 1/12 = 1 + 1/3 = 4/3 hours. The answer is 4/3." + \
					"\nC: The answer is incorrect. Bill takes 10 minutes to run up a hill and 5 minutes to cut a tree. So it takes him 10/60 = 1/6 hours to run up a hill and 5/60 = 1/12 hours to cut a tree. He needs to run up 12 hills and cut 18 trees. So, it will take him 12 * 1/6 + 18 * 1/12 = 2 + 3/2 = 2 + 1.5 = 3.5 hours. The answer is 3.5." + \
					"\nQ: Harry is two feet taller than John, who is three feet shorter than Mary. Mary is four feet taller than Jason. Jason is twice as tall as Gary. If Gary is 3 feet tall, how tall is Harry?" + \
					"\nA: Harry is two feet taller than John and John is three feet shorter than Mary. This means that Harry is 2 + 3 = 5 feet taller than Mary. Mary is four feet taller than Jason. This means that Harry is 5 + 4 = 9 feet taller than Jason. Jason is twice as tall as Gary. This means that Harry is 2 * 9 = 18 feet taller than Gary. Gary is 3 feet tall. This means that Harry is 18 + 3 = 21 feet tall. The answer is 21." + \
					"\nC: The answer is incorrect. Gary is 3 feet tall and Jason is twice as tall as Gary. This means that Jason is 2 * 3 = 6 feet tall. Mary is 4 feet taller than Jason, so Mary is 6 + 4 = 10 feet tall. John is 3 feet shorter than Mary, so John is 10 - 3 = 7 feet tall. Harry is 2 feet taller than John. This means that Harry is 2 + 7 = 9 feet tall. The answer is 9." + \
					"\nQ: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?" + \
					"\nA: There are 3 cars in the parking lot already. 2 more arrive. Now there are 3 + 2 = 5 cars. The answer is 5." + \
					"\nC: The answer is correct." + \
					"\nQ: " + meta_data["Q"] + "\nA: " + meta_data["A"] + "\nC:"
					# "\nQ: Bill had 39 marbles. Jack took five marbles from Bill. If Bill needs to distribute the remaining marbles equally into 2 sets, how many marbles does he need to put in each set?" + \
					# "\nA: Bill had 39 marbles initially and Jack took five of them. This means he had 39 - 5 = 34 marbles remaining. To distribute these marbles into 2 sets equally, he needs to put 34 / 2 = 17 marbles in each set. The answer is 17." + \
					# "\nC: The answer is correct." + \
					# "\nQ: A box can contain 5 envelopes and each envelope can carry 10 papers. If Jack delivers 50 boxes every day, how many papers get delivered every week?" + \
					# "\nA: A box has 5 envelopes and an envelope has 10 papers. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day. This means that in every box, there are 5 envelopes and in every envelope, there are 10 papers. Jack delivers 50 boxes every day." + \
					# "\nC: The answer is incorrect. A box has 5 envelopes and each envelope has 10 papers. This means that each box has 5 * 10 = 50 papers. Jack delivers 50 boxes every day, so he delivers 50 * 50 = 2,500 papers every day. This means that every week, he delivers 7 * 2,500 = 17,500 papers. The answer is 17,500." + \
					# "\nQ: Sam had 39 chocolates. Carl took three chocolates from Sam. If Sam needs to distribute the remaining chocolates equally into 3 boxes, how many chocolates does he need to put in each box?" + \
					# "\nA: Sam needs to distribute the chocolates into three boxes. This means he had 39 / 3 = 13 chocolates in each box. Since Carl took three chocolates, there are 13 - 3 = 10 chocolates. The answer is 10." + \
					# "\nC: The answer is incorrect. Carl took three chocolates from Sam, so Sam has 39 - 3 = 36 chocolates. Sam needs to distribute the chocolates equally into three boxes. So, he needs to put 36 / 3 = 12 chocolates in each box. The answer is 12." + \
	elif prompt_type == "full":
		prompt = "Generate the Output for the corresponding Input:" + \
					"\nInput: lug\nOutput: BLUE" + \
					"\nInput: dax\nOutput: RED" + \
					"\nInput: lug fep\nOutput: BLUE BLUE BLUE" + \
					"\nInput: wif\nOutput: GREEN" + \
					"\nInput: wif blicket dax\nOutput: GREEN RED GREEN" + \
					"\nInput: dax kiki lug\nOutput: BLUE RED" + \
					"\nInput: dax fep\nOutput: RED RED RED" + \
					"\nInput: lug fep kiki wif\nOutput: GREEN BLUE BLUE BLUE" + \
					"\nInput: wif blicket dax kiki lug\nOutput: BLUE GREEN RED GREEN" + \
					"\nInput: zup\nOutput: YELLOW" + \
					"\nInput: lug kiki wif\nOutput: GREEN BLUE" + \
					"\nInput: lug blicket wif\nOutput: BLUE GREEN BLUE" + \
					"\nInput: wif kiki dax blicket lug\nOutput: RED BLUE RED GREEN" + \
					"\nInput: lug kiki wif fep\nOutput: GREEN GREEN GREEN BLUE" + \
					"\nInput: " + df.loc[i]["Input"] + "\nOutput:"
	elif prompt_type == "full-englishy":
		prompt = 	"\nlug is BLUE" + \
					"\ndax is RED" + \
					"\nlug fep is BLUE BLUE BLUE" + \
					"\nwif is GREEN" + \
					"\nwif blicket dax is GREEN RED GREEN" + \
					"\ndax kiki lug is BLUE RED" + \
					"\ndax fep is RED RED RED" + \
					"\nlug fep kiki wif is GREEN BLUE BLUE BLUE" + \
					"\nwif blicket dax kiki lug is BLUE GREEN RED GREEN" + \
					"\nzup is YELLOW" + \
					"\nlug kiki wif is GREEN BLUE" + \
					"\nlug blicket wif is BLUE GREEN BLUE" + \
					"\nwif kiki dax blicket lug is RED BLUE RED GREEN" + \
					"\nlug kiki wif fep is GREEN GREEN GREEN BLUE" + \
					"\n" + df.loc[i]["Input"] + " is"
	elif prompt_type == "short-3-prims-fep-kiki":
		prompt = "Generate the Output for the corresponding Input:" + \
					"\nInput: lug\nOutput: BLUE" + \
					"\nInput: lug fep\nOutput: BLUE BLUE BLUE" + \
					"\nInput: dax\nOutput: RED" + \
					"\nInput: dax kiki lug\nOutput: BLUE RED" + \
					"\nInput: dax fep\nOutput: RED RED RED" + \
					"\nInput: lug fep kiki dax\nOutput: RED BLUE BLUE BLUE" + \
					"\nInput: lug kiki dax\nOutput: RED BLUE" + \
					"\nInput: dax fep kiki lug\nOutput: BLUE RED RED RED" + \
					"\nInput: zup\nOutput: YELLOW" + \
					"\nInput: " + df.loc[i]["Input"] + "\nOutput:"
	elif prompt_type == "short-3-prims-fep-kiki-englishy":
		prompt = 	"\nlug is BLUE" + \
					"\nlug fep is BLUE BLUE BLUE" + \
					"\ndax is RED" + \
					"\ndax kiki lug is BLUE RED" + \
					"\ndax fep is RED RED RED" + \
					"\nlug fep kiki dax is RED BLUE BLUE BLUE" + \
					"\nlug kiki dax is RED BLUE" + \
					"\ndax fep kiki lug is BLUE RED RED RED" + \
					"\nzup is YELLOW" + \
					"\n" + df.loc[i]["Input"] + " is"
	elif prompt_type == "shortest-3-prims-fep-kiki":
		prompt = "Generate the Output for the corresponding Input:" + \
					"\nInput: lug\nOutput: BLUE" + \
					"\nInput: lug fep\nOutput: BLUE BLUE BLUE" + \
					"\nInput: dax\nOutput: RED" + \
					"\nInput: dax kiki lug\nOutput: BLUE RED" + \
					"\nInput: dax fep\nOutput: RED RED RED" + \
					"\nInput: lug kiki dax\nOutput: RED BLUE" + \
					"\nInput: zup\nOutput: YELLOW" + \
					"\nInput: " + df.loc[i]["Input"] + "\nOutput:"
	elif prompt_type == "shortest-3-prims-fep-kiki-englishy":
		prompt = 	"\nlug is BLUE" + \
					"\nlug fep is BLUE BLUE BLUE" + \
					"\ndax is RED" + \
					"\ndax kiki lug is BLUE RED" + \
					"\ndax fep is RED RED RED" + \
					"\nlug kiki dax is RED BLUE" + \
					"\nzup is YELLOW" + \
					"\n" + df.loc[i]["Input"] + " is"
	elif prompt_type == "short-3-prims-kiki":
		prompt = "Generate the Output for the corresponding Input:" + \
					"\nInput: lug\nOutput: BLUE" + \
					"\nInput: dax\nOutput: RED" + \
					"\nInput: dax kiki lug\nOutput: BLUE RED" + \
					"\nInput: lug kiki dax\nOutput: RED BLUE" + \
					"\nInput: zup\nOutput: YELLOW" + \
					"\nInput: " + df.loc[i]["Input"] + "\nOutput:"
	elif prompt_type == "short-3-prims-kiki-englishy":
		prompt = 	"\nlug is BLUE" + \
					"\ndax is RED" + \
					"\ndax kiki lug is BLUE RED" + \
					"\nlug kiki dax is RED BLUE" + \
					"\nzup is YELLOW" + \
					"\n" + df.loc[i]["Input"] + " is"
	elif prompt_type == "wl-iid":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Beaker : b b o o ; Jar : o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o o ; Jar : o ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Jar : b o o ;\nCommand: Unmix Jar \nOutput World State: Jar : b ; Jar : o o ;" + \
					"\nInput World State: Beaker : b o b o ; Jar : o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Beaker : o ; Jar : b o ;\nCommand: Unmix Jar \nOutput World State: Beaker : o ; Jar : b ; Jar : o ;" + \
					"\nInput World State: Jar : b b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Beaker : o b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Destroy Beaker \nOutput World State: Jar : b ;" + \
					"\nInput World State: Beaker : b o ; Jar : o o o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : b o ; Jar : o o o ; Jar : b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ;\nCommand: Add two orange to Jar \nOutput World State: Jar : b o o ;" + \
					"\nInput World State: Beaker : o b ;\nCommand: Unmix Beaker \nOutput World State: Beaker : o ; Beaker : b ;" + \
					"\nInput World State: Beaker : o b ; Jar : b o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : o b ; Jar : b b ; Jar : o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-add-1":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Jar : b o o ;\nCommand: Unmix Jar \nOutput World State: Jar : b ; Jar : o o ;" + \
					"\nInput World State: Beaker : b o b o ; Jar : o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Beaker : o ; Jar : b o ;\nCommand: Unmix Jar \nOutput World State: Beaker : o ; Jar : b ; Jar : o ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Destroy Beaker \nOutput World State: Jar : b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Beaker : o b ;\nCommand: Unmix Beaker \nOutput World State: Beaker : o ; Beaker : b ;" + \
					"\nInput World State: Beaker : o b ; Jar : b o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : o b ; Jar : b b ; Jar : o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-add-3":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Jar : b o o ;\nCommand: Unmix Jar \nOutput World State: Jar : b ; Jar : o o ;" + \
					"\nInput World State: Beaker : b o b o ; Jar : o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Beaker : o ; Jar : b o ;\nCommand: Unmix Jar \nOutput World State: Beaker : o ; Jar : b ; Jar : o ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Destroy Beaker \nOutput World State: Jar : b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : o b ;\nCommand: Unmix Beaker \nOutput World State: Beaker : o ; Beaker : b ;" + \
					"\nInput World State: Beaker : o b ; Jar : b o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : o b ; Jar : b b ; Jar : o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-destroy-1":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Jar : b o o ;\nCommand: Unmix Jar \nOutput World State: Jar : b ; Jar : o o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Beaker : o ; Jar : b o ;\nCommand: Unmix Jar \nOutput World State: Beaker : o ; Jar : b ; Jar : o ;" + \
					"\nInput World State: Jar : b b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Beaker : o b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ;\nCommand: Add two orange to Jar \nOutput World State: Jar : b o o ;" + \
					"\nInput World State: Beaker : o b ;\nCommand: Unmix Beaker \nOutput World State: Beaker : o ; Beaker : b ;" + \
					"\nInput World State: Beaker : o b ; Jar : b o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : o b ; Jar : b b ; Jar : o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-destroy-3":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Jar : b o o ;\nCommand: Unmix Jar \nOutput World State: Jar : b ; Jar : o o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Beaker : o ; Jar : b o ;\nCommand: Unmix Jar \nOutput World State: Beaker : o ; Jar : b ; Jar : o ;" + \
					"\nInput World State: Jar : b b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Beaker : o b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ;\nCommand: Add two orange to Jar \nOutput World State: Jar : b o o ;" + \
					"\nInput World State: Beaker : o b ;\nCommand: Unmix Beaker \nOutput World State: Beaker : o ; Beaker : b ;" + \
					"\nInput World State: Beaker : o b ; Jar : b o b ;\nCommand: Unmix Jar \nOutput World State: Beaker : o b ; Jar : b b ; Jar : o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-unmix-1":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : b o b o ; Jar : o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Jar : b b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Beaker : o b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Destroy Beaker \nOutput World State: Jar : b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ;\nCommand: Add two orange to Jar \nOutput World State: Jar : b o o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	elif prompt_type == "wl-unmix-3":
		prompt = "Generate the Output World State for the corresponding Input World State:" + \
					"\nInput World State: Jar : o b o b ; Beaker : o o ;\nCommand: Add two blue to Jar \nOutput World State: Jar : o b o b b b ; Beaker : o o ;" + \
					"\nInput World State: Jar : b o b o ; Beaker : o b ;\nCommand: Unmix Jar \nOutput World State: Jar : b b ; Jar : o o ; Beaker : o b ;" + \
					"\nInput World State: Beaker : b b ; Jar : o o b ;\nCommand: Destroy Beaker \nOutput World State: Jar : o o b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Add one orange to Beaker \nOutput World State: Jar : b ; Beaker : b o o ;" + \
					"\nInput World State: Beaker : b b o ;\nCommand: Unmix Beaker \nOutput World State: Beaker : b b ; Beaker : o ;" + \
					"\nInput World State: Beaker : b o b o ; Jar : o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b o ;" + \
					"\nInput World State: Beaker : o b ; Jar : o b b ;\nCommand: Add two orange to Jar \nOutput World State: Beaker : o b ; Jar : o b b o o ;" + \
					"\nInput World State: Jar : b b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : o ; Beaker : b o b ;\nCommand: Destroy Jar \nOutput World State: Beaker : b o b ;" + \
					"\nInput World State: Jar : b o ; Beaker : o o b ;\nCommand: Unmix Beaker \nOutput World State: Jar : b o ; Beaker : o o ; Jar : b ;" + \
					"\nInput World State: Beaker : o b ; Beaker : b o b ;\nCommand: Add one blue to Beaker \nOutput World State: Jar : b b ; Beaker : b o b b ;" + \
					"\nInput World State: Jar : b ; Beaker : b o ;\nCommand: Destroy Beaker \nOutput World State: Jar : b ;" + \
					"\nInput World State: Beaker : o o ; Jar : o b b ;\nCommand: Destroy Jar \nOutput World State: Beaker : o o ;" + \
					"\nInput World State: Jar : b ;\nCommand: Add two orange to Jar \nOutput World State: Jar : b o o ;" + \
					"\nInput World State: " + df.loc[i]["Input"].split("SEPARATE")[0].strip() + "\nCommand: " + df.loc[i]["Input"].split("SEPARATE")[1].strip() + "\nOutput World State:"
	
	return prompt

def permute_prompts(base_prompts, num):
	temp_base_prompts_ls = base_prompts.split("\n")[:-2]
	base_prompts_ls = ["\n".join(temp_base_prompts_ls[z:z+2]) for z in range(0, len(temp_base_prompts_ls), 2)]
	combi_ls = [list(y) for y in combinations(base_prompts_ls, num)]
	permute_data = []
	for combi in combi_ls:
		ques_ls = [k for k in base_prompts_ls if k not in combi]
		permute_data.append((combi, ques_ls))
	return permute_data

