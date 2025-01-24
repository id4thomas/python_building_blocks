'''
파이썬 multithreading queue 사용 테스트
'''
import copy
from concurrent.futures import ThreadPoolExecutor
import threading
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
    
'''
# 2. Objects with Queue
* https://stackoverflow.com/questions/41673522/is-python-multiprocessing-queue-safe-for-object-put
    * queue doesn't automatically deep copy
    
## result
```
Object ID in main thread: 4350147936
Object ID in worker: 4350147936

List Example:
Object ID in main thread: 4302707392
Object ID in worker: 4302707392
[1, 2, 3]
```
-> same object
'''
class MyObject:
    def __init__(self, value):
        self.value = value
        
def worker(queue):
    obj = queue.get()
    print(f"Object ID in worker: {id(obj)}")
        
def worker2(queue):
    test_list = queue.get()
    print(f"Object ID in worker: {id(test_list)}")
    test_list.append(3)

def object_id_check():
    q = Queue()
    my_obj = MyObject(42)
    print(f"Object ID in main thread: {id(my_obj)}")
    q.put(my_obj)

    thread = threading.Thread(target=worker, args=(q,))
    thread.start()
    thread.join()

    
    test_list = [1,2]
    print(f"Object ID in main thread: {id(test_list)}")
    q.put(test_list)
    
    thread = threading.Thread(target=worker2, args=(q,))
    thread.start()
    thread.join()
    print(test_list)

if __name__=="__main__":
    queue = Queue()
    
    print("1----use ThreadPoolExecutor")
    use_executor(queue, num_work=200, num_workers=1, max_workers=5)
    use_executor(queue, num_work=200, num_workers=5, max_workers=5)
    
    print("2----Queue Object ID")
    object_id_check()