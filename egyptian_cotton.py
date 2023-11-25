import threading
import time
from math import floor
from random import random

print_lock = threading.Lock()


def ts_print(*args, **kwargs):
    """Thread-safe print"""
    with print_lock:
        print(*args, **kwargs)


range_max = 50
thread_count = 100
ranges = [
    # comment the line out below and `ranges` will fill with `thread_count` random ranges
    [10, 20], [1, 5], [70, 80], [27, 92], [0, 16]
]


def make_ranges(n_ranges):
    if len(ranges):
        return

    for new_range in range(n_ranges):
        h = floor(random() * range_max)
        k = floor(random() * range_max)
        new_range = [min(h, k), max(h, k)]
        ranges.append(new_range)


make_ranges(thread_count)


n_threads = len(ranges)
result = [0] * n_threads

threads = []

elapsed_time_qsum = 0
elapsed_time_sum = 0


def qsum(n):
    return n*(n+1)//2


def sum_range(thread_name: str, range_parameter: range, result_index: int):
    global elapsed_time_sum
    global elapsed_time_qsum

    start, stop = range_parameter
    stop = stop + 1

    start_time_qsum = time.time()
    result[result_index] = qsum(stop) - qsum(start)
    end_time_qsum = time.time()

    start_time_sum = time.time()
    result[result_index] = sum(range(start, stop))
    end_time_sum = time.time()

    dt_qsum = end_time_qsum - start_time_qsum
    dt_sum = end_time_sum - start_time_sum

    elapsed_time_qsum += dt_qsum
    elapsed_time_sum += dt_sum

    # ts_print(f"{thread_name}:\tSum'd range [{start},{stop - 1}]\t->\tr[i]:\t{result[result_index]}\n"
    #          f"\t\tqsum:\t({dt_qsum:.3}s)\t\tsum:\t({dt_sum:.3}s)")


for i in range(n_threads):
    r = ranges[i]
    name = f"T-{i}"
    thread = threading.Thread(target=sum_range, args=(name, r, i))
    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()

result_sum = sum(result)

# print(f"\n------------------------------------------------------------\n"
#      f"Et viola: {n_threads} threads worked out {result_sum:.3f}\n"
#      f"\t\tqsum:\t{elapsed_time_qsum:.3}s,\tsum:\t{elapsed_time_sum:.3}s")

print(result)
print(result_sum)
