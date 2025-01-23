import asyncio
import sys
print(sys.version) # 3.12.1

'''
# Event Loop
* get_event_loop(): 이벤트 루프가 실행중이지 않으면 생성 (3.12 이후 부터는 warning)
* new_event_loop(): 이벤트 루프를 생성하고 반환
* set_event_loop(): 이벤트 루프를 설정
'''
## Check Running loop before init
print("1----CHECK RUNNING LOOP BEFORE INIT")
'''
EVENT LOOP NOT RUNNING
'''
try:
    asyncio.get_running_loop()
    print("EVENT LOOP RUNNING")
except RuntimeError as e:
    print("EVENT LOOP NOT RUNNING")
    print(e)
    
## get event loop without initializing
print("\n\n2----GET EVENT LOOP WITHOUT INITIALIZING")
'''
no running event loop
async_1_run.py:25: DeprecationWarning: There is no current event loop
  loop = asyncio.get_event_loop()
4537653904 <class 'asyncio.unix_events._UnixSelectorEventLoop'> <_UnixSelectorEventLoop running=False closed=False debug=False>
'''
loop = asyncio.get_event_loop()
print(id(loop), type(loop), loop)


## initialize then get
print("\n\n3----INITIALIZE THEN GET")
'''
new 4537714640 <class 'asyncio.unix_events._UnixSelectorEventLoop'> <_UnixSelectorEventLoop running=False closed=False debug=False>
get 4537653904 <class 'asyncio.unix_events._UnixSelectorEventLoop'> <_UnixSelectorEventLoop running=False closed=False debug=False>

<- 'get' gets the event loop created in 2, and set as current event loop
'''
loop = asyncio.new_event_loop()
print("new",id(loop), type(loop), loop)

loop = asyncio.get_event_loop()
print("get",id(loop), type(loop), loop)


'''
# Schedule Tasks
* run(): 이벤트 루프를 실행하고 콜백을 스케줄링
* create_task(): 콜백을 스케줄링
* create_future(): 콜백을 스케줄링
'''
print("\n\n4----SCHEDULE TASKS")
'''
create_task(coroutine): 이벤트 루프 '내부에서' 비동기 작업을 스케쥴링
* get_event_loop() gets loop defined in 2
'''
async def fn(x):
    await asyncio.sleep(x)
    print(f"fn({x})")

async def routine1():
    # Check event loop
    loop = asyncio.get_event_loop()
    print("get",id(loop), type(loop), loop)
    
    # Schedule tasks
    task1 = asyncio.create_task(fn(0.1))
    task2 = asyncio.create_task(fn(0.2))
    task3 = asyncio.create_task(fn(0.3))
    await task1
    await task2
    await task3
asyncio.run(routine1())


'''
# gather vs wait
'''
print("\n\n5-1----GATHER")
async def gather_test():
	results = await asyncio.gather(fn(0.1), fn(0.2))
	print(results)
asyncio.run(gather_test())

print("\n\n5-2----WAIT")
'''
fn(1)
fn(2)
<Task finished name='Task-14' coro=<fn() done, defined at async_1_run.py:61> result=None> None
<Task finished name='Task-13' coro=<fn() done, defined at async_1_run.py:61> result=None> None
'''
async def wait_test():
    tasks = [
        asyncio.create_task(fn(1)),
        asyncio.create_task(fn(2)),
    ]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        print(task, task.result())
asyncio.run(wait_test())


'''
# asyncio create_task후 await와 coroutine을 바로 await 하는 것의 차이
'''
import time
print("\n\n6----CREATE TASK VS COROUTINE")
'''
# create_task -> gather
fn(1)
fn(2)
time: 2.002708911895752

# await
fn(1)
fn(2)
time: 3.0076353549957275
-> create_task 후 gather 할 때 병렬로 실행
'''
async def create_task_test():
    time_start = time.time()
    tasks = [
        asyncio.create_task(fn(1)),
        asyncio.create_task(fn(2)),
    ]
    await asyncio.gather(*tasks)
    time_end = time.time()
    print(f"time: {time_end - time_start}")
asyncio.run(create_task_test())

async def coroutine_test():
    time_start = time.time()
    await fn(1)
    await fn(2)
    time_end = time.time()
    print(f"time: {time_end - time_start}")
asyncio.run(coroutine_test())
