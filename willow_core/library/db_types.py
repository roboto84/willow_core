from typing import TypedDict


class DeleteDbItemResponse(TypedDict):
    deleted_item: bool
    reason: str
    data: list[str]
