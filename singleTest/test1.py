import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    tasks = [say_after(1, 'hello'), say_after(2, 'world')]

    print(f"started at {time.strftime('%X')}")

    await asyncio.gather(*tasks)

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())