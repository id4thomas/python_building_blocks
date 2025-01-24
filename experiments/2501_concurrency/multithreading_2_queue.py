'''
파이썬 multithreading queue 사용 테스트
'''
import threading
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import time

'''
# 1. Queue to distribute work
## result
```
max 5 num work 200
Thread work count 200
num work 200 with 1 threads 2.471
max 5 num work 200
Thread work count 40
Thread work count 40
Thread work count 40
Thread work count 40
Thread work count 40
num work 200 with 5 threads 0.500
```
-> time is almost divided equally (most of it is sleep time)
'''
def compute_factorial(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    # print(f"Factorial of {number} is {result}")
    time.sleep(0.01)
    
def compute_worker(queue):
    thread_work_count = 0
    while not queue.empty():
        number = queue.get()
        compute_factorial(number)
        thread_work_count+=1
        queue.task_done()
    print(f"Thread work count {thread_work_count}")

def use_executor(queue, num_work: int = 100, num_workers = 3, max_workers=3):
    print(f"max {max_workers} num work {num_work}")
    for i in range(num_work):
        queue.put(i)

    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(num_workers):
            executor.submit(compute_worker, queue)
    print(f"num work {num_work} with {num_workers} threads {time.time()-start:.3f}")
    

if __name__=="__main__":
    queue = Queue()
    
    print("1----use ThreadPoolExecutor")
    use_executor(queue, num_work=200, num_workers=1, max_workers=5)
    use_executor(queue, num_work=200, num_workers=5, max_workers=5)