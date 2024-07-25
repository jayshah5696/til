# Notes on algorithms and data structures


## Data structures
- [Notes on algorithms and data structures](#notes-on-algorithms-and-data-structures)
  - [Data structures](#data-structures)
    - [Linked List](#linked-list)
    - [Stack](#stack)
    - [Queue](#queue)
    - [Hash Table](#hash-table)
  - [Algorithms](#algorithms)
    - [Binary Search](#binary-search)
    - [Selection Sort](#selection-sort)
    - [Quick Sort](#quick-sort)
    - [Breadth First Search (BFS)](#breadth-first-search-bfs)


### Linked List
- A linked list is a linear data structure where each element is a separate object.
- Each element (node) of a list is comprising of two items - the data and a reference to the next node.
- The last node has a reference to null.
- The entry point into a linked list is called the head of the list.
- A linked list is a dynamic data structure. The number of nodes in a list is not fixed and can grow and shrink on demand.
- The time complexity of most of the operations like insertion, deletion is O(1), reaching an element in a linked list is O(n).
- Some applications of linked list are:
  - Implementing a stack or queue
  - Symbol table in compilers
  - Dynamic memory allocation

### Stack
- A stack is a linear data structure that follows the Last In First Out (LIFO) principle.
- The main operations are push, pop, and peek.
- The time complexity of all operations is O(1).
- Stack can be implemented using an array or a linked list.
- Some applications of stack are:
  - Function call stack
  - Undo mechanism in text editors
  - Expression evaluation
  - Backtracking

### Queue
- A queue is a linear data structure that follows the First In First Out (FIFO) principle.
- The main operations are enqueue, dequeue, and peek.
- The time complexity of all operations is O(1).
- Queue can be implemented using an array or a linked list.
- Some applications of queue are:
  - CPU scheduling
  - Disk scheduling
  - Breadth First Search (BFS)
  
### Hash Table
- A hash table is a data structure that stores key-value pairs.
- It uses a hash function to compute an index into an array of buckets or slots, from which the desired value can be found.
- The time complexity of all operations is O(1) on average.
- The time complexity of all operations is O(n) in the worst case.
- Some applications of hash table are:
  - Database indexing
  - Caching
  - Symbol table in compilers



## Algorithms

### Binary Search 
- Binary search is a search algorithm that finds the position of a target value within a sorted array.
- The time complexity of binary search is O(log n).
- The array must be sorted before applying binary search.
- The main steps of binary search are:
  - Compare x with the middle element.
  - If x matches with the middle element, we return the mid index.
  - Else if x is greater than the mid element, then x can only lie in the right half subarray after the mid element. So we recur for the right half.
  - Else (x is smaller) recur for the left half.
- Binary search can be implemented using both iterative and recursive approaches.
- The iterative approach is more efficient than the recursive approach because it does not require the overhead of function calls.
```python
def binary_search(arr, x):
    # Iterative approach
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            low = mid + 1
        else:
            high = mid - 1
    return -1

def binary_search(arr, x, low, high):
    # Recursive approach
    if low <= high:
        mid = low + (high - low) // 2
        if arr[mid] == x:
            return mid
        elif arr[mid] < x:
            return binary_search(arr, x, mid + 1, high)
        else:
            return binary_search(arr, x, low, mid - 1)
    return -1
```


### Selection Sort
- Selection sort is a simple sorting algorithm that selects the smallest element from an unsorted list in each iteration and places it at the beginning of the list.
- The time complexity of selection sort is O(n^2).
- The main steps of selection sort are:
  - Find the smallest element in the unsorted list.
  - Swap it with the leftmost unsorted element.
  - Move the subarray boundary one element to the right.
  - Repeat the above steps until the entire list is sorted.
  
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr
```

### Quick Sort
- Quick sort is a divide-and-conquer sorting algorithm that divides an array into two subarrays, then sorts the subarrays independently.
- The time complexity of quick sort is O(n log n) on average and O(n^2) in the worst case.
- The main steps of quick sort are:
  - Pick an element as pivot (usually the last element).
  - Partition the array into two subarrays such that all elements less than the pivot are on the left and all elements greater than the pivot are on the right.
  - Recursively apply quick sort on the left and right subarrays.
  
```python
def quick_sort(arr):
    if len(arr)<=1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + [x for x in arr if x == pivot] + quick_sort(right)
```

### Breadth First Search (BFS)
- Breadth First Search (BFS) is a graph traversal algorithm that explores all vertices in the graph level by level.
- The time complexity of BFS is O(V + E), where V is the number of vertices and E is the number of edges in the graph.
- Application of BFS:
  - Shortest path in an unweighted graph
  - Connected components
  - Level order traversal of a tree
  - finding minimum or shortest path to given problem
- The main steps of BFS are:
  - Start from a source vertex and mark it as visited.
  - Enqueue the source vertex into a queue.
  - While the queue is not empty, dequeue a vertex from the queue.
  - For each adjacent vertex of the dequeued vertex, if it is not visited, mark it as visited and enqueue it into the queue.
  - Repeat the above step until the queue is empty.
  
