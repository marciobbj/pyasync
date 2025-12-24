import pyasync
import requests

async def get_http_data():
    response = await requests.get("https://jsonplaceholder.typicode.com/posts/1")
    if not response.ok:
        raise Exception("you got nothing from response")
    return response.json()


async def get_server_response():
    data = await get_http_data()
    if not data:
        raise Exception("you got nothing from data")
    return data


if __name__ == "__main__":
    data = get_server_response()
    print(data)
