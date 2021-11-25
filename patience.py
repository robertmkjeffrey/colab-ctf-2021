a = 938888977362043978014154482373763
b = 494792124312035773584257506322319129344

not_the_flag = 481883688215427563815801059619186806691721209646


def num_to_flag(n):
    print(n)
    s = ''
    while n > 0:
        s = chr(n%256) + s
        n = n >> 8
    print(s)
    exit()

# The solution!
# The code below finds the largest number that can't be written as ai+bj=n, i,j>0.
# This does it faster :)
num_to_flag(a*b-a-b)

n = a*b
while n > 0:
    found = False
    j = 0
    while b*j <= n: 
        i = 0
        while a*i + b*j < n:
            i += 1
        if a*i + b*j == n:
            found = True
            j = b
            break
        j += 1

    if found:
        n -= 1
    else:
        num_to_flag(n)

num_to_flag(not_the_flag)
