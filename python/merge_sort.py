from copy import copy


def merge_sort(numbers):         
    copy_numbers = copy(numbers)
    swap_count = m_sort(copy_numbers, [None] * len(numbers), 0, len(numbers)-1)
    print (swap_count)
    return copy_numbers

def m_sort(numbers, temp, left, right):    
    if left >= right:
        temp[left] = numbers[left]                  
        return 0                                        
    mid = (right+left)//2
    swap_count1 = m_sort(numbers, temp, left, mid)
    swap_count2 = m_sort(numbers, temp, mid+1, right)
    swap_count3 =  merge(numbers, temp, left, mid+1, right)
    return  swap_count1 + swap_count2 + swap_count3

def merge(numbers, temp, left, mid, right):
    left_end = mid - 1                       
    tmp_pos = left                          
    num_elements = right - left  + 1
    swap_count = 0 
    i, j = 0, 0      
    while(left <= left_end and mid <= right):
        if numbers[left] <= numbers[mid]:      
            temp[tmp_pos] = numbers[left]        
            tmp_pos += 1                    
            left += 1 
            swap_count += j
        else:         
            j += 1
            temp[tmp_pos] = numbers[mid]
            tmp_pos += 1                
            mid += 1
    if left <= left_end:
        temp[tmp_pos: tmp_pos + left_end - left] = numbers[left: left_end + 1]
        tmp_pos += (left_end - left)
    if mid <= right:
        temp[tmp_pos: tmp_pos + right - mid] = numbers[mid: right + 1]
             
    numbers[right - num_elements + 1: right + 1] = temp[right - num_elements + 1: right + 1]
    return swap_count

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        numbers = list(map(int, sys.argv[1:]))
        sorted_list = merge_sort(numbers)
        print(sorted_list)
    else:
        numbers = input("Please enter space seperated numbers: ")
        numbers = list(map(int, numbers.strip().split(' ')))
        sorted_list = merge_sort(numbers)
        print (sorted_list)