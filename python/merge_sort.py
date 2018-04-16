def merge_sort(numbers):         
    m_sort(numbers, [None] * len(numbers), 0, len(numbers)-1)

def m_sort(numbers, temp, left, right):    
    if left >= right:
        temp[left] = numbers[left]                  
        return                                          
    mid = (right+left)//2
    m_sort(numbers, temp, left, mid)
    m_sort(numbers, temp, mid+1, right)
    merge(numbers, temp, left, mid+1, right)

def merge(numbers, temp, left, mid, right):
    left_end = mid - 1                       
    tmp_pos = left                          
    num_elements = right - left  + 1        
    while(left <= left_end and mid <= right):
        if numbers[left] <= numbers[mid]:      
            temp[tmp_pos] = numbers[left]        
            tmp_pos += 1                    
            left += 1                       
        else:         
            temp[tmp_pos] = numbers[mid]
            tmp_pos += 1                
            mid += 1                    
    while left <= left_end:
        temp[tmp_pos] = numbers[left]
        left += 1                    
        tmp_pos += 1                 
    while mid <= right:
        temp[tmp_pos] = numbers[mid]
        mid += 1                    
        tmp_pos += 1                
    for i in range(num_elements):
        numbers[right] = temp[right]
        right -= 1

if __name__ == "__main__":
    import sys
    print (sys.argv)
    if len(sys.argv) > 1:
        numbers = list(map(int, sys.argv[1:]))
        merge_sort(numbers)
        print(numbers)
    else:
        numbers = input("Please enter space seperated numbers")
        numbers = list(map(int, numbers.strip().split(' ')))
        merge_sort(numbers)
        print (numbers)