import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def bubbleSort(arr):
    n = len(arr)
    for i in range(n-1):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
            yield arr

def insertionSort(arr):
    n = len(arr)
    for i in range(n):
        j = i
        while j > 0 and arr[j] < arr[j-1]:
            arr[j], arr[j-1] = arr[j-1], arr[j]
            j = j-1
            yield arr

def mergeSort(arr, start, end):
    def merge(arr, start, mid, end):
        result = []
        left_index = start
        right_index = mid + 1
        while left_index <= mid and right_index <= end:
            if arr[left_index] < arr[right_index]:
                result.append(arr[left_index])
                left_index+=1
            else:
                result.append(arr[right_index])
                right_index+=1
    
        while left_index <= mid:
            result.append(arr[left_index])
            left_index+=1
    
        while right_index <= end:
            result.append(arr[right_index])
            right_index+=1
    
        for index, value in enumerate(result):
            arr[start+index] = value
            yield arr

    if end <= start:
        return
    mid = start + ((end-start+1)//2)
    yield from mergeSort(arr, start, mid-1)
    yield from mergeSort(arr, mid, end)
    yield from merge(arr, start, mid-1, end)
    yield arr
    
def quickSort(array, start, end):
    if start >= end:
        return
    pivot = array[start]
    j = start
    for i in range(start+1, end+1):
        if array[i] <= pivot:
            j += 1
            array[j], array[i] = array[i], array[j]
        yield array
    array[start], array[j],  = array[j], array[start]
    yield array
 
    yield from quickSort(array, start, j-1)
    yield from quickSort(array, j+1, end)

def heapSort(arr, n):
    # put root into the right place to adjust heap to a max heap
    def adjust(arr, root, n):
        # child = left child of root
        child = root*2+1
        while child < n:
            # let child be the bigger child
            if child+1 < n and arr[child+1] > arr[child]:
                child += 1
            # go deeper child if child were bigger than root
            if arr[child] > arr[(child-1)//2]:
                arr[(child-1)//2], arr[child] = arr[child], arr[(child-1)//2]
                child = child*2+1
                yield arr
            else:
                break

    # heap sort
    # build max heap
    for i in range((n-1-1)//2,-1,-1):
        yield from adjust(arr, i, n)
    # sort
    for i in range(n-1,-1,-1):
        arr[0], arr[i] = arr[i], arr[0]
        yield arr
        yield from adjust(arr,0,i)

def update_fig(array, rects, iteration, title, id):
    x = id // 3
    y = id % 3

    ax[x,y].set_title(title)
    for rect, val in zip(rects[id], array):
        rect.set_height(val)
    iteration[id] += 1
    text[id].set_text(f"iterations: {iteration[id]}")

# main
# constant
data_num = 50
sorting_num = 6

# prepare the arrays to be sorted
array = [[None]] * sorting_num
array[0] = [i+1 for i in range(data_num)]
random.shuffle(array[0])
for i in range(1,sorting_num):
    array[i] = array[i-1].copy()

# init subplots
fig, ax = plt.subplots(2,3)
for x in range(2):
    for y in range(3):
        ax[x,y].set_xlim(0, data_num)
        ax[x,y].set_ylim(0, int(1.1*data_num))  # y軸高一點比較好看
        ax[x,y].set_xticklabels([])  # x, y軸都不顯示標籤
        ax[x,y].set_yticklabels([])

bar_rects = [ax[x,y].bar(range(data_num), array[x*3 + y], align="edge") for x in range(2) for y in range(3)]
text = [ax[x,y].text(0.03, 0.91, "", transform = ax[x,y].transAxes) for x in range(2) for y in range(3)]



iteration = [0] * 6
anim = [None] * 6

id = 0
anim[id] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "bubble sort", id), frames=bubbleSort(array[id]), interval=1, repeat=False)
id = 1
anim[id] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "insertion sort", id), frames=insertionSort(array[id]), interval=1, repeat=False)
id = 2
anim[id] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "merge sort", id), frames=mergeSort(array[id],0,data_num-1), interval=1, repeat=False)
id = 3
anim[id] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "quick sort", id), frames=quickSort(array[id],0,data_num-1), interval=1, repeat=False)
id = 4
anim[id] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "heap sort", id), frames=heapSort(array[id],data_num), interval=1, repeat=False)

plt.show()