import sys
import os
import pyasync


async def func_with_some_io():
    await pyasync.sleep(1)
    return {"data": "this is the data you want"}


async def get_example_values():
    c = await func_with_some_io()
    if not c:
        raise Exception("you got nothing from c")
    return c


if __name__ == "__main__":
    data = get_example_values()
    print(data)
