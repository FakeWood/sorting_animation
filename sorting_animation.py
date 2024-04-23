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
array = [] * sorting_num
array[0] = [i+1 for i in range(data_num)]
random.shuffle(0)
for i in range(1,sorting_num):
    array[i] = array[i-1].copy()

# init subplots
fig, ax = plt.subplots(2,3)
for x in range(2):
    for y in range(3):
        ax[x,y].set_xlim(0, data_num)
        ax[x,y].set_ylim(0, int(1.1*data_num))  # y軸高一點比較好看
bar_rects = [ax[x,y].bar(range(data_num), array, align="edge") for x in range(2) for y in range(3)]
text = [ax[x,y].text(0.03, 0.91, "", transform = ax[x,y].transAxes) for x in range(2) for y in range(3)]



iteration = [0] * 6
anim = [None] * 6

anim[0] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "bubble sort", 0), frames=bubbleSort(array), interval=1, repeat=False)

anim[1] = FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration, "insertion sort", 1), frames=insertionSort(array), interval=1, repeat=False)



plt.show()