# vim: ts=4 sw=0 sts=-1 et ai tw=80

"""
Group class
"""

import math, itertools
from perm import Perm

# TODO: write dummy tests
# TODO: Probably make Group aware of which symmetric group it's embedded in.

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

    def is_group(self):
        """
        Check that self is actually a group.

        This seems to check rather fewer axioms than are normally stated for
        groups. The reason is that we needn't check associativity since the
        operation is composition of permutations, which is always associative,
        and since we have proved closure and we know all permutations have
        finite order, this guarantees the existence of inverses, since
        sigma^{ord(sigma) - 1} must also lie in the group.
        """
        return self.perms and self.is_closed()


    def is_subgroup(self, other):
        """
        Check if self is a subgroup of other (not if it's isomorphic to a
        subgroup. If you know it's closed and non-empty, just use
        perms.issubset).
        """
        # TODO: perhaps make this function aware of the usual canonical
        #       embedding of S_n into S_{n + 1}.
        return self.perms.issubset(other.perms) and self.is_group()

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
        Returns the dihedral group of order 2n.
        """
        # if n <= 2:
        #     return Group.cyclic(n) ** 2
        rots = cls.cyclic(n).perms
        refls = {Perm(n)(tuple((j - i) % n for i in range(n)))
                    for j in range(n)}
        return cls(rots | refls)

    @classmethod
    def symmetric(cls, n):
        return cls(set(map(Perm(n), itertools.permutations(range(n)))))

    def order_sequence(self):
        """
        Return the order sequence of the group as a list
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

    def __mul__(self, other):
        """Returns the direct product of this group and another"""
        # Wow okay gross
        for a in self.perms:
            break
        for b in other.perms:
            break
        self_padded_perms = [g.pad_after(len(b)) for g in self.perms]
        other_padded_perms = [g.pad_before(len(a)) for g in other.perms]
        return type(self)({g * h for g in self_padded_perms
                                 for h in other_padded_perms})

    def automorphism_group(self):
        """
        Return the automorphism group of the group
        """
        pass

    def is_isomorphism(self, other, mapping):
        """
        Check if the function mapping defines an isomorphism from this group to
        another
        """
        return all((mapping(g) * mapping(h) == mapping(g * h) for
                g in self.perms for h in self.perms))

    def is_isomorphic(self, other):
        """
        Check if two groups are isomorphic,
        I thought this would be hard lol
        """
        if self.order_sequence() != other.order_sequence():
            return False
        tuple_perms = tuple(self.perms)
        for tuple_mapping in itertools.permutations(other.perms):
            if self.is_isomorphism(other, lambda g:
                    tuple_mapping[tuple_perms.index(g)]):
                return True
        return False

    def __str__(self):
        """
        String representation with disjoint cycle decompositions.
        """
        return "{{{}}}".format(", ".join(map(str, self.perms)))

    def __len__(self):
        """
        Return the order of self
        """
        return len(self.perms)

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
    # this is bad
    print(Group.dihedral(2))
    print(Group.cyclic(2))
    print("Hopefully all true:")
    print(H.is_group())
    print(all(Group.dihedral(k).is_group() for k in range(1, 10)))
    print(all(Group.cyclic(k).is_group() for k in range(1, 10)))
    print(all(Group.cyclic(k).is_subgroup(Group.dihedral(k)) for k in range(1, 10)))
    # yikes
    print(all(not Group.dihedral(k).is_subgroup(Group.cyclic(k)) for k in range(3, 10)))
    print(all(len(Group.cyclic(k)) == k for k in range(1, 10)))
    # yikes
    print(all(len(Group.dihedral(k)) == 2 * k for k in range(3, 10)))
    print(all(len(Group.symmetric(k)) == math.factorial(k) for k in range(8)))
    print(all(Group.cyclic(k).is_subgroup(Group.symmetric(k)) for k in range(1, 10)))
    print(all(Group.dihedral(k).is_subgroup(Group.symmetric(k)) for k in range(3, 10)))
