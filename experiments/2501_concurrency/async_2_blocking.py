'''
비동기 코드 + blocking 코드 테스트
'''
import asyncio
import concurrent.futures
import sys
import time
from typing import Literal
print(sys.version) # 3.12.1

# Init event loop
loop = asyncio.new_event_loop()
print("loop:",id(loop), type(loop), loop)

'''
# 비동기 코드 내부에서 blocking 실행을 하는 경우
* blocking_test에서는 blocking -> gather를 시도
    * **gather 시간 + blocking** 시간 만큼 소요
* non_blocking_test 에서는 blocking operation을 별도 스레드로 분리
    * **max(gather 시간, blocking 시간)** 만큼 소요
'''
print("1----Blocking inside async code")
'''
non-blocking test
blocking A-4 started!
non_blocking 1-1 started!
non_blocking 2-2 started!
non_blocking 1-1 finished! 1.001
non_blocking 2-2 finished! 2.001
blocking task A-4 finished 4.005
thread: Elapsed: 4.007
process: Elapsed: 4.107 (new process overhead)

blocking test
Running blocking task...
blocking A-4 started!
blocking task A-4 finished 4.005
non_blocking 1-1 started!
non_blocking 2-2 started!
non_blocking 1-1 finished! 1.001
non_blocking 2-2 finished! 2.001
Elapsed: 6.007

process 시도시 오류 발생:
RuntimeError: 
An attempt has been made to start a new process before the
current process has finished its bootstrapping phase.

This probably means that you are not using fork to start your
child processes and you have forgotten to use the proper idiom
in the main module:

if __name__ == '__main__':
    freeze_support()
    ...
concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly while the future was running or pending.
-> 
'''

async def non_blocking_fn(name, delay):
    print(f"non_blocking {name}-{delay} started!")
    start = time.time()
    await asyncio.sleep(delay)  # 비동기 방식으로 지연
    print(f"non_blocking {name}-{delay} finished! {time.time()-start:.3f}")

def blocking_fn(name, delay):
    print(f"blocking {name}-{delay} started!")
    start = time.time()
    time.sleep(delay)
    print(f"blocking task {name}-{delay} finished {time.time()-start:.3f}")

async def blocking_test():
    print("\nblocking test")
    task1 = asyncio.create_task(non_blocking_fn("1", 1))
    task2 = asyncio.create_task(non_blocking_fn("2", 2))
    start = time.time()
    print("Running blocking task...")
    blocking_fn("A", 4)
    
    await asyncio.gather(task1, task2)
    print(f"Elapsed: {time.time()-start:.3f}")
    
async def non_blocking_test(method: Literal["process", "thread"]="thread"):
    loop = asyncio.get_event_loop()

    print(f"\nnon-blocking test {method}")
    task1 = asyncio.create_task(non_blocking_fn("1", 1))
    task2 = asyncio.create_task(non_blocking_fn("2", 2))
    start = time.time()
    if method=="thread":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            await loop.run_in_executor(executor, blocking_fn, "A", 4)
    else:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            await loop.run_in_executor(executor, blocking_fn, "A", 4)
        
    await asyncio.gather(task1, task2)
    print(f"Elapsed: {time.time()-start:.3f}")
   
if __name__ == "__main__": 
    asyncio.run(non_blocking_test(method="thread"))
    asyncio.run(non_blocking_test(method="process"))
    asyncio.run(blocking_test())