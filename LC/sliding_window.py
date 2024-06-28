"""
Q1. Longest Substring Without Repeating Characters
Description
Given a string s, find the length of the longest substring without repeating characters.

Example 1
input: "abcabcbb"
output: 3

Example 2
input: "bbbbb"
output: 1

Example 3
input: "pwwkew"
output: 3
"""

def find_max_substring(string_input):
    # with sliding window
    n = len(string_input)
    if n<=1:
        return n
    left = 0
    right = 0
    max_length = 0
    char_set = set()
    while right<n:
        if string_input[right] not in char_set:
            char_set.add(string_input[right])
            right+=1
            max_length = max(max_length,right-left)
        elif string_input[right] in char_set:
            char_set.remove(string_input[left])
            left+=1
    return max_length


"""
Q2. Minimum Size Subarray Sum
Description
Given an array of positive integers nums and a positive integer target, 
return the minimal length of a contiguous subarray 
[numsl, numsl+1, ..., numsr-1, numsr] of which 
the sum is greater than or equal to target.
If there is no such subarray, return 0 instead.

Example 1
input: target = 7, nums = [2,3,1,2,4,3]
output: 2

Example 2
input: target = 4, nums = [1,4,4]
output: 1
"""

# contiguous mean that the subarray should be continuous
# o(n2) solution
def find_min_list(nums, target):
    n = len(nums)
    for window in range(2,len(nums)+1):
        if window==n:
            return window
        for i in range(n-window+1):
            if sum(nums[i:i+window])>=target:
                return window
            

# o(n) solution

def find_min_list(nums, target):
    n = len(nums)
    left = total =0
    min_length=n+1
    for right in range(n):
        total+=nums[right]
        while total>=target:
            min_length = min(right-left+1,min_length)
            total-= nums[left]
            left+=1
    return min_length if min_length!=n+1 else 0