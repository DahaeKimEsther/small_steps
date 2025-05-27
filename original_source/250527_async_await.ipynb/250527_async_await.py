import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what, time.strftime('%X'))

async def sync_example():
    print(f"started at {time.strftime('%X')}")

    await say_after(3, 'hello') # await만 사용 시 순차진행
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")
    
async def async_example():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")
    
    await task1 # 동시에 진행
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(sync_example())
print('='*30)
asyncio.run(async_example())