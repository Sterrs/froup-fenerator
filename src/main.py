from group import Group, subsets
from perm import Perm

if __name__ == "__main__":
    # H = Group.cyclic(3)
    # K = G.direct_product(H)
    # for perm in K.perms:
    #     print(perm)
    # H = Group.symmetric(6)
    # for perm in H.perms:
    #     print(perm)
    # print(H.is_closed())
    # print(len(H.perms))
    i = 0
    for G in Group.of_order(5):
        i += 1
        print("Group", i)
        for perm in G.perms:
            print(perm)
        print()

