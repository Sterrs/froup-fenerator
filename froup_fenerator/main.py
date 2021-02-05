from itertools import combinations
from functools import reduce
from operator import mul
from math import factorial, inf
from time import time

from group import Group
from perm import conjugacy_class, canonical_of_cycle_type
from primes import prime_factors, factors

# TODO: argparse
n = 8
UPDATE_INTERVAL = 10 ** 5

def upper_bound_generating_set(n):
    """
    Estimate an upper bound for the integer k such that any group of order n has
    a generating subset of size at most k.

    Estimated by prime factorising n and adding together the exponents of each
    prime.

    The correctness of this bound may be reasoned as follows:

    Let G be a group of order n. Let g_0 be the identity 1 in G, and
    inductively, for each i, set H_i = <g_1, ... g_i>. Choose a g_{i + 1} not in
    H_i. Then the order of H_{i + 1} is a proper multiple of the order of H_i,
    by Lagrange's theorem. Say that r is the least integer such that H_r = G.
    We can write
    |G| = (|H_r| / |H_{r - 1}|) (|H_{r - 1}| / |H_{r - 2}|)
          ... (|H_2| / |H_1|) (|H_1| / |H_0|)
    ie |G| is a product of r nonunit integers, by construction. By considering
    prime factorisations it follows that r is at most the number of prime
    factors that |G| has, counted with multiplicity.

    For p-groups, groups of order 2p, and probably some other classes, this
    bound can be shown to be tight. Sadly we know that the only group of order
    15 is Z/15Z, which is generated by one element.
    """
    return sum(1 for _ in prime_factors(n))

def good_cycle_types(n, lengths):
    """
    Get cycle types in S_n which are composed of cycles from given lengths

    I really don't trust this recursive approach, let's either rewrite or test
    it a lot
    """
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
    return reduce(mul, range(k + 1, n + 1), 1) // factorial(n - k)

def groups_of_order(n):
    start_time = time()
    k = upper_bound_generating_set(n)
    print("Computing usable permutations...")
    good_cts = good_cycle_types(n, list(factors(n))[1:])
    if k == 1:
        valid_perms = []
    else:
        perm_sets = [conjugacy_class(n, ct) for ct in good_cts]
        valid_perms = set().union(*perm_sets)
    print("Finished computing usable permutations!")
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
                print(f"{i:{len(str(N))}}/{N} ({i / N:7.2%}) "
                    f"{i / elapsed if elapsed != 0.0 else inf:.0f}/s"
                    f" ETA{(N - i) * elapsed / i / 60:.0f}m"
                    f" ({(N - i) * elapsed / i / 60 ** 2:.1f}h)"
                    f" {total_groups}G")
            i += 1

if __name__ == "__main__":
    D6 = Group.dihedral(3)
    C2 = Group.cyclic(2)
    D12 = Group.dihedral(6)
    print("D6 * C2 ~= D12 is", D12.is_isomorphic(C2*D6))
    unique = []
    for i, G in enumerate(groups_of_order(n)):
        for H in unique:
            if G.is_isomorphic(H):
                break
        else:
            unique.append(G)
    for i, G in enumerate(unique, 1):
        assert G.is_closed()
        print("Group", i)
        for perm in G.perms:
            print(perm)
        print(perm)

