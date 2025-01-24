'''
파이썬 multithreading 코드 테스트
'''
import threading
from concurrent.futures import ThreadPoolExecutor
import time

## Example function
def compute_factorial(number):
    result = 1
    for i in range(1, number + 1):
        result *= i
    # print(f"Factorial of {number} is {result}")
    time.sleep(0.1)

def no_threads(num_workers: int = 5):
    start = time.time()
    for i in range(num_workers):
        compute_factorial(3)
    print(f"{num_workers} no threads {time.time()-start:.3f}")

'''
# 1. threading.Thread 인스턴스 직접 선언

## results
```
5 no threads 0.519
5 threads 0.106
```
'''

def manual_threads(num_threads: int = 5):
    threads = []
    start = time.time()
    for i in range(num_threads):
        thread = threading.Thread(target=compute_factorial, args=(3,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    print(f"{num_threads} threads {time.time()-start:.3f}")
    
'''
# 2. ThreadPoolExecutor 사용
옵션 `max_workers=None, thread_name_prefix='', initializer=None, initargs=()`
* max_workers: 기본 None 이거나 주어지지 않았다면, 기본값으로 기계의 프로세서 수에 5 를 곱한 값

## result
```
max 3 num 5
5 executor 0.205
max 5 num 5
5 executor 0.106
```
'''
def use_executor(num_threads: int = 5, max_workers=3):
    print(f"max {max_workers} num {num_threads}")
    start = time.time()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(num_threads):
            executor.submit(compute_factorial, i)
    print(f"{num_threads} executor {time.time()-start:.3f}")

if __name__=="__main__":
    print("1----manually use Thread")
    no_threads(5)
    manual_threads(5)
    
    print("2----use ThreadPoolExecutor")
    use_executor(num_threads=5, max_workers=3)
    use_executor(num_threads=5, max_workers=5)