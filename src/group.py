# vim: ts=4 sw=0 sts=-1 et ai tw=80

"""
Group class
"""

import math, itertools
from perm import Perm

def smallest_factor(n):
    i = 2
    while n % i != 0:
        i += 1
    return i


def subsets(s):
    """I don't care that this is bad"""
    if len(s) == 0:
        yield s
        return
    a = s.pop()
    for t in subsets(s):
        yield t
        r = t.copy()
        r.add(a)
        yield r


# Superceded by itertools.combinations
def recursive_choose(s, n):
    """I don't care that this is bad"""
    if n < 0:
        return
    if len(s) == n:
        yield s
        return
    a = s.pop()
    yield from choose(s.copy(), n)
    for t in choose(s.copy(), n-1):
        t.add(a)
        yield t


class Group:
    """
    An object representing a group, in the form of a set of permutations
    """
    def __init__(self, perms=set()):
        self.perms = perms

    def is_closed(self):
        """Check that the group is closed under multiplication"""
        return all(((perm1 * perm2 in self.perms) for perm1 in self.perms for
                perm2 in self.perms))

    def is_subgroup(self, other):
        """Check if self is a subgroup of other (not if it's isomorphic to a
        subgroup. If you know it's closed, just use perms.issubset"""
        return other.perms.issubset(self.perms) and self.is_closed()

    @classmethod
    def cyclic(cls, n):
        """Returns the cyclic group of order n"""
        a = Perm.from_cycle((i for i in range(n)))
        return cls({a**i for i in range(n)})

    @classmethod
    def dihedral(cls, n):
        """Returns the dihedral group of order 2n"""
        r = Perm.from_cycle((i for i in range(n)))
        s = Perm({i:-i % n for i in range(n)})
        return cls({a * (r ** i) for i in range(n) for a in {Perm(), s}})

    @classmethod
    def symmetric(cls, n):
        return cls.generate(Perm.from_cycle((1, 2)),
                            Perm.from_cycle(tuple(range(1, n+1))))

    def order_sequence(self):
        """Return as a list the order sequence of the group"""
        return sorted((a.order() for a in self.perms))

    def on_ints(self, start=0):
        """Convert all perms to be on the integers, starting at a given value

        Returns a set of perms and the number of different integers used
        """
        keys = {}
        for perm in self.perms:
            for key in perm.mapping.keys():
                if key not in keys:
                    keys[key] = start
                    start += 1

        return {perm.apply_mapping(keys) for perm in self.perms}, start

    def direct_product(self, other):
        """Returns the direct product of this group and another"""
        elements1, start = self.on_ints()
        elements2, _ = other.on_ints(start)
        return type(self)({a * b for a in elements1 for b in elements2})

    def automorphism_group(self):
        """Return the automorphism group of the group"""
        pass

    def is_isomorphic(self, other):
        """Check if two groups are isomorphic, this is hard lol"""
        pass

    @classmethod
    def generate(cls, *elements, limit=None):
        """Generate more elements from some generating elements"""
        i = 1
        Id = Perm()
        G = cls(set([Id]))
        to_multiply = [Id]
        new = []
        while len(to_multiply) != 0:
            for a in to_multiply:
                for b in elements:
                    c = a * b
                    if c not in G.perms:
                        i += 1
                        if limit is not None and i > limit:
                            return None
                        G.perms.add(c)
                        new.append(c)
            to_multiply = new
            new = []
        return G
        # for h in elements:
        #     gh = g * h
        #     if gh in self.perms:
        #         continue
        #     self.perms.add(gh)
        #     if limit is not None:
        #         if limit < len(self.perms):
        #             return False
        #     if not self.generate_from(gh, *elements, limit=limit):
        #         return False
        # return True

    @classmethod
    def of_order(cls, n):
        k = int(n/smallest_factor(n))
        N = math.comb(math.factorial(n), k)
        i = 0
        for perms in itertools.combinations(cls.symmetric(n).perms, k):
            i += 1
            G = cls.generate(*perms, limit=n)
            if G is not None and len(G.perms) == n:
                yield G
            print(i, "subsets checked out of", N)

    @classmethod
    def generated_by(cls, n):
        """Subgroups of S_n generated by m elements"""
        pass
