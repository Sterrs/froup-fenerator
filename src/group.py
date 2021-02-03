# vim: ts=4 sw=0 sts=-1 et ai tw=80

"""
Group class
"""

import math, itertools
from perm import Perm

# TODO: write dummy tests

class Group:
    """
    An object representing a group, in the form of a set of permutations
    """
    def __init__(self, perms={}):
        self.perms = perms

    def is_closed(self):
        """
        Check that the group is closed under multiplication
        """
        return all(perm1 * perm2 in self.perms
                    for perm1 in self.perms for perm2 in self.perms)

    def is_subgroup(self, other):
        """
        Check if self is a subgroup of other (not if it's isomorphic to a
        subgroup. If you know it's closed, just use perms.issubset
        """
        return other.perms.issubset(self.perms) and self.is_closed()

    @classmethod
    def cyclic(cls, n):
        """
        Returns the cyclic group of order n
        """
        return cls({Perm(n)(tuple((j + i) % n for i in range(n)))
                    for j in range(n)})

    @classmethod
    def dihedral(cls, n):
        """
        Returns the dihedral group of order 2n
        """
        rots = cls.cyclic(n).perms
        refls = {Perm(n)(tuple((j - i) % n for i in range(n)))
                    for j in range(n)}
        return cls(rots | refls)

    @classmethod
    def symmetric(cls, n):
        return cls(set(map(Perm(n), itertools.permutations(range(n)))))

    def order_sequence(self):
        """
        Return list the order sequence of the group as a list
        """
        return sorted(a.order() for a in self.perms)

    # def on_ints(self, start=0):
    #     """Convert all perms to be on the integers, starting at a given value

    #     Returns a set of perms and the number of different integers used
    #     """
    #     keys = {}
    #     for perm in self.perms:
    #         for key in perm.mapping.keys():
    #             if key not in keys:
    #                 keys[key] = start
    #                 start += 1
    #     return {perm.apply_mapping(keys) for perm in self.perms}, start

    # def __mul__(self, other):
    #     """Returns the direct product of this group and another"""
    #     elements1, start = self.on_ints()
    #     elements2, _ = other.on_ints(start)
    #     return type(self)({a * b for a in elements1 for b in elements2})

    def automorphism_group(self):
        """
        Return the automorphism group of the group
        """
        pass

    def is_isomorphic(self, other):
        """
        Check if two groups are isomorphic, this is hard lol
        """
        pass

    def __str__(self):
        return "{{{}}}".format(", ".join(map(str, self.perms)))

    @classmethod
    def generate(cls, n, elements, limit=math.inf):
        """
        Generate more elements from some generating elements
        """
        i = 1
        Id = Perm(n)()
        G = cls({Id})
        to_multiply = [Id]
        new = []
        while len(to_multiply) != 0:
            for a in to_multiply:
                for b in elements:
                    c = a * b
                    if c not in G.perms:
                        i += 1
                        if i > limit:
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

if __name__ == "__main__":
    H = Group.symmetric(6)
    print(len(H.perms))
    print("Hopefully all true:")
    print(H.is_closed())
    print(all(Group.dihedral(k).is_closed() for k in range(1, 10)))
    print(all(Group.cyclic(k).is_closed() for k in range(1, 10)))
