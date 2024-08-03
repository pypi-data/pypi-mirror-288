from typing import Any
from collections import deque
from queue import Queue, PriorityQueue
import heapq

# ListNode, Tree 需要自定义
# stack（LIFO）就是用list实现的
# queue（FIFO）就是用queue实现的, 也可以用list实现, 但是效率不高。线程安全
# deque（双端队列）就是用deque实现的， 可以从左边插入和删除，也可以从右边插入和删除
# priority_queue（优先队列）就是用PriorityQueue实现的，可以设置优先级
# min_heap（最小堆）就是用heapq实现的，可以实现最小堆
# max_heap（最大堆）就是用heapq实现的，可以实现最大堆，只需要把值取负数
# hash_map（哈希表）就是用dict实现的


class xrListNode:
    def __init__(self, value: Any, next=None):
        self.value = value
        self.next = next


class xrTree:
    def __init__(self, value: Any, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class xrStack:
    def __init__(self):
        self.stack = []

    def push(self, value: Any):
        self.stack.append(value)

    def pop(self):
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0


class xrQueue:
    def __init__(self):
        self.queue = Queue()

    def push(self, value: Any):
        self.queue.put(value)

    def pop(self):
        return self.queue.get()

    def is_empty(self):
        return self.queue.empty()


class xrDeque:
    def __init__(self):
        self.deque = deque()

    def push_left(self, value: Any):
        self.deque.appendleft(value)

    def pop_left(self):
        return self.deque.popleft()

    def push_right(self, value: Any):
        self.deque.append(value)

    def pop_right(self):
        return self.deque.pop()

    def is_empty(self):
        return len(self.deque) == 0


class xrPriorityQueue:
    def __init__(self):
        self.priority_queue = PriorityQueue()

    def push(self, value: Any, priority: int):
        self.priority_queue.put((priority, value))

    def pop(self):
        return self.priority_queue.get()[1]

    def is_empty(self):
        return self.priority_queue.empty()


class xrMinHeap:
    def __init__(self):
        self.heap = []

    def push(self, value: Any):
        heapq.heappush(self.heap, value)

    def pop(self):
        return heapq.heappop(self.heap)

    def is_empty(self):
        return len(self.heap) == 0


class xrMaxHeap:
    def __init__(self):
        self.heap = []

    def push(self, value: Any):
        heapq.heappush(self.heap, -value)

    def pop(self):
        return -heapq.heappop(self.heap)

    def is_empty(self):
        return len(self.heap) == 0


class xrHashMap:
    def __init__(self):
        self.hash_map = {}

    def put(self, key: Any, value: Any):
        self.hash_map[key] = value

    def get(self, key: Any):
        return self.hash_map[key]

    def remove(self, key: Any):
        del self.hash_map[key]

    def is_empty(self):
        return len(self.hash_map) == 0
