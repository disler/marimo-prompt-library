Find the bug in this code:

def mult_and_sum_array(arr, multiple):
    multi_arr = [x * multiple for x in arr]
    sum = 0
    sum = sum(multi_arr)
    return sum