def quicksort(array):
    pivot = len(array) - 1
    iterator = 0
    if len(array) == 0:
        return []
    if len(array) == 1:
        return array
    if len(array) == 2:
        if array[0] > array[1]:
            return [array[1], array[0]]
        return array

    while pivot > iterator:
        if array[pivot] < array[iterator]:
            [array[pivot-1], array[pivot]] = [array[pivot], array[pivot - 1]]
            if array[pivot] < array[iterator]:
                [array[iterator], array[pivot]] = [array[pivot], array[iterator]]
            pivot -= 1
        else:
            iterator += 1

    return quicksort(array[:pivot]) + [array[pivot]] + quicksort(array[pivot+1:])
    