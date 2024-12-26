"""
Fairly fast moo algo using binary conversion

This program plays mastermind automatically in a feedback loop. 
The variables trials, correct_positions and correct_numbers are used to memorize what was learned from the previous trials.

The generate_combination function uses the knowledge stored in these variables to develop the programs next guess.

The find_correct_position_or_number function provides automatic feedback to the program to gain more knowledge with each turn. 

This version converts the input and returns the result in binary. 

Due to the fact that only 2 digits are used in processing both the feedback and the next guess, 
this solution is more efficient on larger numbers but may be slower on shorter combinations.
"""

import random
import time
from collections import defaultdict

userinput = input("Enter a combination of digits 0-9")

combination = f"{userinput:b}"

def generate_combination(length):
    return "".join([random.randint(0,1) for _ in range(0,length)])

trials = []
correct_positions = dict()
correct_numbers = defaultdict(set)

last_guess = []


def generate_combination(length:int) -> str:
    res = [ random.randint(0,1) for _ in range(0,length)]
    occupied_indizies = set()
    for key, value in correct_positions.items():
        res[key] = value
        occupied_indizies.add(key)
    for value, false_indezies in correct_numbers.items():
        impossible_indizies = occupied_indizies.union(false_indezies)
        if last_index_trial := [a for a in range(0,length) if a not in impossible_indizies]:        
            res[last_index_trial[-1]]=value
    
    return "".join(res) if res not in trials else generate_combination(length)
    

def find_correct_position_or_number(trial) -> None:
    for index, (a,b) in enumerate(zip(combination, trial)):
        if b in combination:
            correct_numbers[b].add(index)

        if a != b or index in correct_positions:
            continue
        correct_positions[index] = b
        
start = time.time()
while combination != last_guess:
    trial= generate_combination(len(combination))

    find_correct_position_or_number(trial)
    trials.append(trial)
    last_guess = trial
end = time.time()

print(f"The combination is [{''.join(last_guess)}] and it took {len(trials)} trials in {end-start} seconds.")
print(f"Your input was {''.join(combination)}")