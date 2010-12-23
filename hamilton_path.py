#!/usr/bin/python

# Graph represented as Adjacency List
Graph = {
    1:(2,5,20),
    2:(1,3,12),
    3:(2,4,10),
    4:(3,5,8),
    5:(1,4,6),
    6:(5,7,19),
    7:(6,8,17),
    8:(4,7,9),
    9:(8,10,16),
    10:(3,9,11),
    11:(10,12,15),
    12:(2,11,13),
    13:(12,14,20),
    14:(13,15,18),
    15:(11,14,16),
    16:(9,15,17),
    17:(7,16,18),
    18:(14,17,19),
    19:(6,18,20),
    20:(1,13,19),
}

Graph2 = {
    1:(2,5,6),
    2:(1,3,5),
    3:(2,4),
    4:(3,5),
    5:(1,2,4),
    6:(1,),
}

def dfs(graph, vertex, S=[]):
    S.append(vertex)
    for u in graph[vertex]:
        if u not in S:
            dfs(graph, u, S)
    return S

def rec_dfs(G, s, S=None):
    if S is None: S = set()
    S.add(s)
    for u in G[s]:
        if u in S: continue
        rec_dfs(G, u, S)

def build_candidates(graph, vertex, solution=[], candidates=[]):
    candidates.append(vertex)
    for u in graph[vertex]:
        if u not in solution:
            build_candidates(graph, u, solution, candidates)
    return candidates

def backtrack(graph, vertex, solution=[]):
    if len(solution) == 20:
        print(solution)
        return
    else:
        for v in build_candidates(graph, vertex, solution):
            solution.append(v)
            backtrack(graph, v, solution)
            solution.pop()

# print(backtrack(Graph, 2))
print(dfs(Graph, 2))
