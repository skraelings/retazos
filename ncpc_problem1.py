#!/usr/bin/python3
## # -*- coding: utf-8 -*-
"""
2010 (c) Reynaldo Baquerizo <reynaldomic001@gmail.com>

The king in Utopia  has died without an heir. Now several  nobles in the country
claim the  throne. The country  law states  that if the  ruler has no  heir, the
person  who is  most related  to the  founder of  the country  should  rule.  To
determine who is most  related we measure the amount of blood  in the veins of a
claimant that  comes from the  founder.  A person  gets half the blood  from the
father and the other half from the mother. A child to the founder would have 1/2
royal blood, that child’s child with  another parent who is not of royal lineage
would have  1/4 royal  blood, and  so on. The  person with  most blood  from the
founder is the one most related.

Input specifications 
The first line  contains two integers, N (2 ≤ N  ≤ 50) and M (2 ≤  M ≤ 50).  The
second line  contains the name of the  founder of Utopia.  Then  follows N lines
describing a  family relation.  Each such line  contains three  names, separated
with a single space.  The first name is a child and  the remaining two names are
the parents  of the child.  Then follows  M lines containing the  names of those
who  claims the  throne.   All names  in  the input  will be  between  1 and  10
characters long  and only  contain the lowercase  English letters  ’a’-’z’.  The
founder will  not appear  among the claimants,  nor be  described as a  child to
someone else.
"""
from __future__ import print_function
import sys

def parse_sample_data(fd):
    (n, m) = fd.readline().strip().split()
    founder = fd.readline().strip()
    family_tree = {}
    for i in range(int(n)):
        line = fd.readline().strip().split()
        assert len(line) == 3
        child, parents = line[0], tuple(line[1:])
        # child, *parents = line
        family_tree[child] = parents
    claimants = []
    for i in range(int(m)):
        line = fd.readline().strip().split()
        assert len(line) == 1
        claimants.append(line[0])
    return (founder, claimants, family_tree)

def find_all_paths(graph, start, end, path=[]):
    """
    Determines all posible paths between two nodes.
    (Taken from http://python.org/doc/essays/graphs.html)
    """
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start): # python2
    # if not start in graph.keys():
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def main(fd):
    founder, claimants, graph = parse_sample_data(fd)
    # print("Claimant", "|", "Consanguiniedad")
    # print("--------", "-", "---------------")
    # for claimant in claimants:
    #     print(claimant, "|", sum(1/(len(i) - 1) ** 2 for i in
    #                              find_all_paths(graph, claimant, founder)))
    results = [(claimant, sum(1.0/(len(i) - 1) ** 2 
                              for i in find_all_paths(graph, claimant, founder)))
               for claimant in claimants]
    # http://stackoverflow.com/questions/613183/python-sort-a-dictionary-by-value
    import operator
    sorted_results = sorted(dict(results).items(), key=operator.itemgetter(1))
    return sorted_results[-1][0]

if __name__ == '__main__':
    # sys.exit(main(open(sys.argv[1])))
    main(open("/home/rbm/ncpc_sample1.txt"))
