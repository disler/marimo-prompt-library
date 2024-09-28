Find the bug in this code:

def find_max(nums):
    max_num = float('-inf')
    for num in nums:
        if num < max_num:
            max_num = num
    return max_num