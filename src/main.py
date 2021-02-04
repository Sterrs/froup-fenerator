from itertools import combinations
from functools import reduce
from operator import mul
from math import factorial
from time import time

# TODO: portable alternative
from sympy import factorint, divisors

from group import Group
from perm import conjugacy_class, canonical_of_cycle_type

n = 6
UPDATE_INTERVAL = 10 ** 5

def smallest_factor(n):
    i = 2
    while n % i != 0:
        i += 1
    return i

def good_cycle_types(n, lengths):
    """Get cycle types in S_n which are composed of cycles from given lengths"""
    if len(lengths) == 0:
        return [[]]
    m = lengths[0]
    i = 0
    cycle_types = []
    while i * m <= n:
        for cycle_type in good_cycle_types(n - i*m, lengths[1:]):
            cycle_types.append(i * [m] + cycle_type)
        i += 1
    if cycle_types == []:
        return [[]]
    return cycle_types

# my version of PyPy is too old for math.comb
def comb(n, k):
    k = max(k, n - k)
    return reduce(mul, range(k + 1, n + 1)) // factorial(n - k)

def groups_of_order(n):
    start_time = time()
    k = sum(factorint(n).values())
    print("Computing usable permutations...")
    good_cts = good_cycle_types(n, divisors(n)[1:])
    perm_sets = [conjugacy_class(n, ct) for ct in good_cts]
    valid_perms = set().union(*perm_sets)
    print("Finished computing usable permutations!")
    if k == 1:
        N = len(good_cts)
    else:
        N = len(good_cts) * comb(len(valid_perms), k-1)
    total_groups = 0
    i = 1
    for ct in good_cts:
        x = canonical_of_cycle_type(n, ct)
        for perms in combinations(valid_perms, k-1):
            G = Group.generate(n, (x,) + perms, limit=n)
            if G is not None and len(G.perms) == n:
                yield G
                total_groups += 1
            if i % UPDATE_INTERVAL == 0 or i == N or i == 1:
                elapsed = time() - start_time
                print(f"{i:{len(str(N))}}/{N} ({i / N:7.2%}) {i / elapsed:.0f}/s"
                    f" ETA{(N - i) * elapsed / i / 60:.0f}m"
                    f" ({(N - i) * elapsed / i / 60 ** 2:.1f}h)"
                    f" {total_groups}G")
            i += 1

if __name__ == "__main__":
    # for cycle_type in good_cycle_types(12, divisors(12)[1:]):
    #     print(cycle_type)
    # H = Group.symmetric(6)
    # print(H.is_closed())
    # for perm in H.perms:
    #     print(perm, perm.cycle_type())
    # print(len(H.perms))
    # print(all(Group.dihedral(k).is_closed() for k in range(1, 10)))
    # print(all(Group.cyclic(k).is_closed() for k in range(1, 10)))
    for i, G in enumerate(groups_of_order(n)):
        pass
        #print("Group", i)
        #for perm in G.perms:
        #    print(perm)
        #print()

