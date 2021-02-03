from itertools import combinations
from functools import reduce
from operator import mul
from math import factorial
from time import time

# TODO: portable alternative
from sympy import factorint

from group import Group

n = 6
UPDATE_INTERVAL = 10 ** 5

def smallest_factor(n):
    i = 2
    while n % i != 0:
        i += 1
    return i

# my version of PyPy is too old for math.comb
def comb(n, k):
    k = max(k, n - k)
    return reduce(mul, range(k + 1, n + 1)) // factorial(n - k)

def groups_of_order(n):
    start_time = time()
    k = sum(factorint(n).values())
    N = comb(factorial(n), k)
    total_groups = 0
    for i, perms in enumerate(combinations(Group.symmetric(n).perms, k), 1):
        G = Group.generate(n, perms, limit=n)
        if G is not None and len(G.perms) == n:
            yield G
            total_groups += 1
        if i % UPDATE_INTERVAL == 0 or i == N or i == 1:
            elapsed = time() - start_time
            print(f"{i:{len(str(N))}}/{N} ({i / N:7.2%}) {i / elapsed:.0f}/s"
                  f" ETA{(N - i) * elapsed / i / 60:.0f}m"
                  f" ({(N - i) * elapsed / i / 60 ** 2:.1f}h)"
                  f" {total_groups}G")

if __name__ == "__main__":
    H = Group.symmetric(6)
    # print(H.is_closed())
    print(len(H.perms))
    for i, G in enumerate(groups_of_order(n)):
        pass
        # print("Group", i)
        # for perm in G.perms:
        #     print(perm)
        # print()

