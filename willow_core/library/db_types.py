from typing import TypedDict


class DbItemResponse(TypedDict):
    reason: str
    data: list[str]


class AddDbItemResponse(DbItemResponse):
    added_item: bool


class UpdateDbItemResponse(DbItemResponse):
    updated_item: bool


class DeleteDbItemResponse(DbItemResponse):
    deleted_item: bool
