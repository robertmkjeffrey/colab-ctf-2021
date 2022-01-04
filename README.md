# ANU-ASD Colab CTF 2021

This repo is my writeup of the Colab CTF 2021, hosted by the Australian Signals Directorate (ASD) and the Australian National University (ANU). 
We finished 5th, which I'm proud of for what was all of our first CTF! 
Of this, I was the lead solver on four main (classes) of problems: union, mastermind, patience, and the butter overflow series.

## Mastermind

This problem was solved by only one other team and was way more challenging than I expected!

The flag was obtained by solving (a version of) the game "Mastermind". In this game, one individual thinks of a number of a fixed length (6 in our case). 
The guesser then takes turns proposing possible answers. They recieve in return two numbers. First, how many digits are in the correct spot? Secondly, how many digits are correct but in the wrong position?

For example, if the real number is 121583 and the guesser guessed 110153 the response would be 2 correct, 2 close. Another way to frame this is that the "close" digits are the total number of shared digits between both numbers (unordered) minus the number of correct digits.

To get the flag, you needed to win (by guessing the correct number) within 6 turns. My first instinct was to approach it from an information theory perspective and trying to maximise the entropy of my guesses. 
Apon looking for an algorithm; I found one by [Donald Knuth](https://en.wikipedia.org/wiki/Mastermind_(board_game)#Worst_case:_Five-guess_algorithm).
This algorithm essentially works by guessing the combination that is *guarenteed* to eliminate the most options; a minimax strategy that *maximises* the *minimum* number of possible numbers that will be eliminated.

This approach was interesting, but my initial experiments quickly proved intractable. There are 10^6 possible combinations. The most efficient way to find the minimax strategy is to iterate through all 10^6 combinations for each of the 10^6 possible guesses, leading to several days worth of computation for just the first turn!
There were possible ways to speed this up using the symmetries of the problem (In the first turn, we can freely permute the specific digits without changing the optimality of the solution) but I overall thought there was more to it.

In the meanwhile, I continued playing the bot by hand. I noticed two main things:
1. It was quite easy to win the game in ~7 guesses. However I would weirdly always lose in the last turn, even if there were only two possible numbers left. The statistical unlikeliness of this made me test it further and I found that the bot's responses were determanistic: the same sequence of guesses would always lead to the same outcome! Not only that, but if I ran identical sequences but changed the final guess I would still lose. This made me realise that the bot was cheating - it slowly narrowed down the possible field of combinations according to what information it had released. This meant we had to play provably worst-case optimal and justified using Knuth's algorithm.
2. The numbers the bot provided were always ordered. This greatly decreases the number of possible combinations; from 1,000,000 to 5,005. Given the computation is O(n^2) with regards to the number of possible combinations, this made the problem tractible again.

With these two in mind, I implemented the solution in [`mastermind.py`](mastermind.py). The solution maintains a list of all combinations consistent with the guesses so far.
It solves for the optimal guess by first iterating through all possible guesses. For each guess, it considers each combination that remains. It calculats the correct & close results that would come back and counts how many combiantions would return each set of results. Finally, it takes the maximum of these numbers. This gives the worst-case number of combinations remaining if you make that guess.
Once it computes this for all guesses, it chooses the guess with the smallest worst-case number of combinations remaining. This is eqivilent to Knuth's most worst-case eliminations.

Beating the bot took ~10 minutes on my old and slow machine. This could definitely have been reduced by implementing the program in C or Go (especially if it was then parallelised), but the speedup wouldn't have justified the significantly increased development time. 

Overall, this was one of the more challenging problem I tackled during the CTF and the many development hours made it all the more satisfying to see the bot concede defeat!

## Patience
Patience was a challenge released halfway through the competition. The puzzle provided a python script that performed an extremely slow computation ([`patience.py`](patience.py)). Upon seeing this, I immediately noted it as calculating the smallest number not divisible by coprime interegers a and b. This can be calculated directly as $ab-a-b$. Adding this line of code gave the flag almost instantly.

## Union
Union was the "one that got away". I ended up getting quite close to the final solution; but couldn't spot the closed-form solution for the algorithm I developed. However, I'm quite proud of the work I managed and think I could have reached it had I experimented more.

The Union line started with lineup ([`lineup.py`](lineup.py)). This was a version of the classic white hats - black hats game. There are 100 logicians in a line each with a hat labelled 0-3. The logicians can see all hats in front of them, but not their own. How can they guess their own hat colour?

The solution is a simple modification of the original version: the first logician sums the hat numbers in front of him modulo 4 and guesses this as his hat number. Each logician in front then computes this same sum. By comparing this to the previous calls, they can compute their own hat number. An implementation can be seen in [`lineup.lua`](lineup.lua).

The union problems modified this in a unique way. Now there are 99 logicians and 100 hats labelled, without repetition, 0-99. Importantly, no two logicians can ever call the same hat number. There were three levels; save 49 logicians, save 96, and save 98.

The 49 level was relatively straightforward; the first 49 logicians look at the logician 50 steps ahead of them. They then guess the lowest the hat number above that logician's hat that is also not the hat of one of the last 49 logicians. This avoids repeats while allowing the logicians to figure out the intended hat. An implementation can be seen in [`union.lua`](union.lua).

The 98 level was the next step I approached. As the first logician cannot get his hat consistently right, this essentially means the first logician is the only source of information that must allow all remaining logicians to guess the right hat. This strictness has a benefit however; as all 98 logicians must get their hats correct, we can essentially treat it all all 98 logicians being able to see each other's hats. We then need to figure out how to provide a single call, from the two possible hats not present on those 98, that uniquely determines the sequence.

I started from small hat counts to try and find an algorithm. We can represent this as finding a function that maps a list to a single number; the hat the first logician calls out. We'll call this function f(x1, x2, ..., xn). 

For a mapping to work, each logician must be able to uniquely identify their hat based on all other logicians' hats in addition to the "revealled" hat. Formally, the function g(y) = f(x1, x2, ..., y, ... xn) must be injective for fixed x1 ... xn.

In small hat counts, we can use this to manually define the mapping. For four logicians and four hats, we need to save 2. Defining the mapping as follows:

f(0, 1) = 3

f(0, 2) = 1

f(0, 3) = 2

f(1, 0) = 2

f(1, 2) = 3

f(1, 3) = 0

f(2, 0) = 3

f(2, 1) = 0

f(2, 3) = 1

f(3, 0) = 1

f(3, 1) = 2

f(3, 2) = 0

satisfies this property. This property allows us to generate the entire mapping off one single decision, and thus would have let us solve the problem. Unfortunately I wasn't competent enough in Lua to solve it within the time frame. 
