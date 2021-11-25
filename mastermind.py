# %%
import itertools
from tqdm import tqdm
from collections import defaultdict
digits = range(10)
all_guesses = list(itertools.combinations_with_replacement(digits, 6))
possibilities = set(itertools.combinations_with_replacement(digits, 6))

# %%
def score_guess(guess, code):
    i = 0
    j = 0
    correct_count = sum(1 if guess[i] == code[i] else 0 for i in range(len(guess)))
    
    total_count = 0

    while True:

        if i == len(guess):
            break
        if j == len(guess):
            break

        a=guess[i]
        b=code[j]

        if a < b:
            i += 1
        elif a > b:
            j += 1
        elif a == b:
            i += 1
            j += 1
            total_count += 1
    return correct_count, (total_count-correct_count)

# Unit test
assert score_guess((4,4,4,7,8,9), (4,6,6,8,9,9)) == (2,1)


# %%
def update_consistent(guess, correct, close):
    global possibilities
    new_possibilities = set()
    for code in possibilities:
        if score_guess(guess, code) == (correct, close):
            new_possibilities.add(code)
    possibilities = new_possibilities

# %%

def solve():

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

def stringToTuple(string):
    return [int(x) for x in string]

# %%

while True:
    try:
        guess = solve()
    except KeyboardInterrupt:
        guess = stringToTuple(input("Enter guess instead:"))
    
    print(guess)

    correct = int(input("Correct?: "))
    close = int((input("Close?: ")))

    if correct == 6:
        print("Poggers!")
        print("🎉🎉🎉")

    update_consistent(guess, correct, close)
 
