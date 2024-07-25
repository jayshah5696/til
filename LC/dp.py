"""
Q1. Climb Stairs
Description
You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?

Example 1
input = 2 
output = 2

Example 2
input = 3
output = 3

Example 3
input = 10
output = 89
"""

def climb_stairs(n):
    if n<=3:
        return n
    dp = [0]*n+1
    dp[1]=1
    dp[2]=2
    dp[3]=3
    for i in range(4,n+1):
        dp[i] = dp[i-1]+dp[i-2]
    return dp[n]



"""
Q2 House Robber
Description
You are a professional robber planning to rob houses along a street. 
Each house has a certain amount of money stashed. 
All houses at this place are arranged in a circle.
That means the first house is the neighbor of the last one.
Meanwhile, adjacent houses have a security system connected, and
it will automatically contact the police if two adjacent houses were broken into
on the same night.
Given a list of non-negative integers nums representing the amount of money of each house,
return the maximum amount of money you can rob tonight without alerting the police.

Example 1
input: [2,3,2]
output: 3
Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.

Example 2
input: [1,2,3,1]
output: 4

"""
def total_money(input):
    n = len(input)
    if n<=2:
        return max(input)
    dp = [0]*n
    dp[0]=input[0]
    dp[1]=max(input[0],input[1])
    for i in range(2,n):
        if i!=n:
            dp[i] = max(dp[i-1],dp[i-2]+input[i])
    return dp[-1]



"""
279. Perfect Squares
Description
Given a positive integer n, find the least number of perfect square numbers
(for example, 1, 4, 9, 16, ...) which sum to n.

Example 1
input: 12
output: 3
Explanation: 12 = 4 + 4 + 4.

Example 2
input: 13
output: 2
Explanation: 13 = 4 + 9.
"""


def perfect_squqre(n):
    dp = [0]* (n+1)
    for i in range (1,n+1):
        dp[i] = i
        j = 1
        while j*j <=i:
            dp[i] = min(dp[i],dp[i-j*j]+1)
            j+=1
    return dp[n]
    



# finding common maximum substring between two strings


def find_max_substring(str1, str2):
    n = len(str1)
    m = len(str2)
    dp = [[0]*(m+1) for _ in range(n+1)]
    max_length = 0
    for i in range(1,n+1):
        for j in range(1,m+1):
            if str1[i-1]==str2[j-1]:
                dp[i][j] = dp[i-1][j-1]+1
                max_length = max(max_length,dp[i][j])
    return max_length