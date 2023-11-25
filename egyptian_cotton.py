import threading
import time

ranges = [
    [1, 5],
    [10, 20],
    [1, 3]
]

n_threads = len(ranges)
result = [0] * n_threads

threads = []


def sum_range(r):
    start, stop = r
    return sum(range(start, stop))


for i in range(n_threads):
    r = ranges[i]
    thread = threading.Thread(target=sum_range, args=(r,))
    thread.start()

    threads.append(thread)

for thread in threads:
    thread.join()





