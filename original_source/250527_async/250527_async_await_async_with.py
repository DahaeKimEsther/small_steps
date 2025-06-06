import asyncio
import time
# Follow numbers: 1., ... 2., ...

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what, time.strftime('%X'))

async def sync_example():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello') # 2. await만 사용 시 순차진행
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")
    
async def async_example():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")
    await task1 # 3. asyncio.create_task()로 만들어진 task들은 동시에 진행됨
    await task2
    print(f"finished at {time.strftime('%X')}")

async def async_with_example():
    async with asyncio.TaskGroup() as tg: # 4. async with는 Task Group에 정의된 task들의 aenter, aexit()를 처리함
        task1 = tg.create_task(say_after(1, 'hello'))
        task2 = tg.create_task(say_after(2, 'world'))
        print(f"started at {time.strftime('%X')}")
    print(f"finished at {time.strftime('%X')}")

# 1. asyncio.run() function to run the top-level entry point, for example, sync_example()
asyncio.run(sync_example())
print('='*30)
asyncio.run(async_example())
print('='*30)
asyncio.run(async_with_example())