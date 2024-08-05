from pydantic import BaseModel, HttpUrl
from typing import Optional, List, TypeVar, Generic


class Link(BaseModel):
    href: Optional[HttpUrl] = None


class PaginationLinks(BaseModel):
    next: Optional[Link] = None
    previous: Optional[Link] = None
    self: Link


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    _links: PaginationLinks
    count: int
    data: List[T]
