
"""
Q1 
Description
Given a positive integer n, return the minimum number of step to reduce n to 0.
In one step, you can add or subtract a power of two (2^i, i >= 0).

Example 1

Input: 14
Output: 2
Explanation: 14(01110) -> 16(10000) -> 0
Example 2

Input: 27
Output: 3
Explanation: 27(011011) -> 31(011111) -> 32(100000) -> 0
Example 3

Input: 1
Output: 1
"""

from collections import deque

def min_integers(input):
    queue = deque([(input,0)])
    visited = set()

    node, state = queue.popleft()
    visited.add(node)
    while node!=0:
        i=0
        if node==0:
            return state
        while (1<<i) <=node:
            next_positives = node+(1<<i)
            next_negatives = node-(1<<i)
            if next_positives not in visited:
                queue.append((next_positives, state+1))
                visited.add(next_positives)
            if next_negatives not in visited:
                queue.append((next_negatives, state+1))
                visited.add(next_negatives)
            i+=1
        node, state = queue.popleft()
    return state

# some comments
# << operation is bit shift operation in python


"""
Q2 Knight;s shortest path in chessboard of n x n

input : n = 8, start = [0,0], end = [7,7]
output: 6

Input : n=64, start = [0,0], end = [63,7]
output: 32

Input : n=8, start = [0,0], end = [3,3]
output: 2
"""

def shortest_path(input,output):
    directions = [(2,1),(-2,1),(2,-1),(-2,1),(1,2),(-1,2),(1,-2),(-1,-2)]

    queue = deque([(input,0)])
    visited = set()
    node, state = queue.popleft()
    visited.add(node)

    while node!=output:
        for direction in directions:
            next_node = (node[0]+direction[0],node[1]+direction[1])
            if next_node not in visited:
                queue.append((next_node, state+1))
                visited.add(next_node)
        node, state = queue.popleft()

    return state

# some comments
# directions are how possible state changes. 


"""
2285. Maximum Total Importance of Roads
Description
You are given an integer n denoting the number of cities in a country. The cities are numbered from 0 to n - 1.
You are also given a 2D integer array roads where roads[i] = [ai, bi] denotes that there exists a bidirectional road connecting cities ai and bi.
You need to assign each city with an integer value from 1 to n, where each value can only be used once. The importance of a road is then defined as the sum of the values of the two cities it connects.
Return the maximum total importance of all roads possible after assigning the values optimally.

Example 1
n = 5, roads = [[0,1],[1,2],[2,3],[0,2],[1,3],[2,4]]
importance = {0:2,1:4,2:5,3:3,4:1}
output = 43

Example 2 
n = 5 , roads = [[0,3],[2,4],[1,3]]
importance = {0:4,2:2,3:5,3:1,4:1}
output = 20
"""

# you need to figure out importance of each city as how many times it is 

def importance(n,roads):
    visits = {i:0 for i in range(n)}
    for a,b in roads:
        visits[a]+=1
        visits[b]+=1
    # the way of sorting by values item: item[1]
    sorted_visits =dict(sorted(visits.items(),key= lambda item:item[1] ,reverse=True))
    # other way
    # sorted_cities = sorted(range(n), key=lambda x: visits[x], reverse=True)
    
    importance = {}
    for i,city in enumerate(sorted_visits.keys()):
        importance[city] = n-i
    return importance


def max_imp_of_roads(n,roads):
    importance_ = importance(n,roads)
    total_imp = 0
    for a, b in roads:
        total_imp+=importance_[a]+importance_[b]
    return total_imp



    
