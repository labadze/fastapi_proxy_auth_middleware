# import os
import os
from typing import Union

import httpx
from fastapi.encoders import jsonable_encoder

from core.schemas import ItemResponseCollectionBase, SuccessResponseSchema, ItemBodySchema, User, ItemInsertSchema

# httpx_async_client = httpx.AsyncClient(base_url=os.getenv("API_URL"))
httpx_async_client = httpx.AsyncClient(http2=True)


async def retrieve_item_list(limit: int, offset: int, access_token: str) -> list[ItemResponseCollectionBase]:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }
    params = {'limit': limit, 'offset': offset}
    response = await httpx_async_client.get(
        url="{back_end_url}/protected/items".format(back_end_url=os.getenv("BACK_END_URL")),
        headers=headers, params=params)
    return response.json()


async def fetch_single_item(item_id: str, access_token: str) -> ItemResponseCollectionBase:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }
    response = await httpx_async_client.get(url="{back_end_url}/protected/items/{item_id}"
                                            .format(back_end_url=os.getenv("BACK_END_URL"), item_id=item_id),
                                            headers=headers)
    return response.json()


async def delete_single_item(item_id: str, access_token: str) -> SuccessResponseSchema:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }
    response = await httpx_async_client.delete(url="{back_end_url}/protected/items/{item_id}"
                                               .format(back_end_url=os.getenv("BACK_END_URL"), item_id=item_id),
                                               headers=headers)
    return response.json()


async def update_single_item(item_id: str, data: ItemBodySchema, access_token: str) -> SuccessResponseSchema:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }
    body_json = jsonable_encoder(data)
    response = await httpx_async_client.put(url="{back_end_url}/protected/items/{item_id}"
                                            .format(back_end_url=os.getenv("BACK_END_URL"), item_id=item_id),
                                            headers=headers, json=body_json)
    return response.json()


async def insert_single_item(data: ItemInsertSchema, access_token: str) -> SuccessResponseSchema:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }
    body_json = jsonable_encoder(data)
    response = await httpx_async_client.post(url="{back_end_url}/protected/items"
                                             .format(back_end_url=os.getenv("BACK_END_URL")),
                                             headers=headers, json=body_json)
    return response.json()


async def fetch_current_user_from_back_end(access_token: str) -> Union[User, None]:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }

    response = await httpx_async_client.get(
        url="{back_end_url}/private/account".format(back_end_url=os.getenv("BACK_END_URL")),
        headers=headers)
    print(response.json())
    return response.json()


async def end_session(access_token: str, user_id: str) -> SuccessResponseSchema:
    headers = {
        'content-type': 'application/json',
        'Authorization': "Bearer {token}".format(token=access_token)
    }

    response = await httpx_async_client.get(
        url="{back_end_url}/private/account/destroy_token/{user_id}".format(back_end_url=os.getenv("BACK_END_URL"),
                                                                            user_id=user_id), headers=headers)
    return response.json()
