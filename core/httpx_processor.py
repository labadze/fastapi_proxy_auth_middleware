# import os

import httpx

# httpx_async_client = httpx.AsyncClient(base_url=os.getenv("API_URL"))
httpx_async_client = httpx.AsyncClient()


async def end_session(logout_url: str):
    headers = {
        'content-type': 'application/json'
    }
    response = await httpx_async_client.get(url=logout_url, headers=headers)
    print(response)
