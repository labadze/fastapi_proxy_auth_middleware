import typing

from fastapi import Depends, APIRouter

from core.dependencies import check_http_cookies
from core.httpx_processor import delete_single_item, retrieve_item_list, fetch_single_item, update_single_item, \
    insert_single_item
from core.schemas import ItemInsertSchema, ItemBodySchema, ItemResponseCollectionBase, SuccessResponseSchema

router = APIRouter(
    prefix="/protected",
    tags=["items"],
    dependencies=[Depends(check_http_cookies)],
    responses={404: {"description": "Not found"}},
)


@router.get("/items", tags=["items"], response_model=list[ItemResponseCollectionBase], status_code=200)
async def retrieve_items(limit: int, offset: int, user_data: typing.Any = Depends(check_http_cookies)):
    return await retrieve_item_list(limit=limit, offset=offset, access_token=user_data.access_token)


@router.get("/items/{item_id}", tags=["items"], response_model=ItemResponseCollectionBase, status_code=200)
async def fetch_item(item_id: str, user_data: typing.Any = Depends(check_http_cookies)):
    return await fetch_single_item(item_id=item_id, access_token=user_data.access_token)


@router.put("/items/{item_id}", tags=["items"], response_model=ItemResponseCollectionBase, status_code=200)
async def update_item(item_id: str, body: ItemBodySchema, user_data: typing.Any = Depends(check_http_cookies)):
    update_data = ItemBodySchema(
        entry_value=body.entry_value,
        is_active=body.is_active,
        rate=body.rate,
        carma=body.carma,
    )
    return await update_single_item(item_id=item_id, data=update_data, access_token=user_data.access_token)


@router.delete("/items/{item_id}", tags=["items"], response_model=SuccessResponseSchema, status_code=200)
async def delete_item(item_id: str, user_data: typing.Any = Depends(check_http_cookies)):
    await delete_single_item(item_id=item_id, access_token=user_data.access_token)
    return {
        "success": True,
        "message": "Item was deleted successfully"
    }


@router.post("/items", tags=["items"], response_model=ItemResponseCollectionBase, status_code=201)
async def insert_item(body: ItemBodySchema, user_data: typing.Any = Depends(check_http_cookies)):
    item_insert_data = ItemInsertSchema(
        entry_value=body.entry_value,
        is_active=body.is_active,
        rate=body.rate,
        carma=body.carma,
        user_id=user_data.user_id
    )
    return await insert_single_item(data=item_insert_data, access_token=user_data.access_token)
