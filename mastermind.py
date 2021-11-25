# %%
import itertools
from tqdm import tqdm
from collections import defaultdict
digits = range(10)
all_guesses = list(itertools.combinations_with_replacement(digits, 6))
possibilities = set(itertools.combinations_with_replacement(digits, 6))

def score_guess(guess, code):
    i = 0
    j = 0
    count = 0
    while True:

        if i == len(guess):
            return count
        if j == len(guess):
            return count

        a=guess[i]
        b=code[j]

        if a < b:
            i += 1
        elif a > b:
            j += 1
        elif a == b:
            i += 1
            j += 1
            count += 1

def update_consistent(guess, score):
    global possibilities
    new_possibilities = set()
    for code in possibilities:
        if score_guess(guess, code) == score:
            new_possibilities.add(code)
    possibilities = new_possibilities

# %%

def solve():

    if len(possibilities) == len(all_guesses):
        return (0,0,1,1,2,2) # TODO - make general
    best_guess = []
    best_score = 0
    minmax_remaining = len(possibilities)
    for guess in tqdm(all_guesses):
        score_map = defaultdict(lambda: 0)
        for code in possibilities:
            score_map[score_guess(guess, code)] += 1
        
        max_remaining = max(score_map.values())
        if max_remaining < minmax_remaining:
            best_guess = [guess]
            minmax_remaining = max_remaining
        elif max_remaining == minmax_remaining:
            best_guess.append(guess)
    
    if len(set(best_guess).intersection(possibilities)):
        return list(set(best_guess).intersection(possibilities))[0]
    else:
        return best_guess[0]

# %%

def check_guess(guess):
    score_map = defaultdict(lambda: 0)
    for code in possibilities:
        score_map[score_guess(guess, code)] += 1
        
    print(score_map)

# %%

solve()

# %%
while True:

    score = input("Score: ")

    update_consistent(guess, score)



# %%

# %%
