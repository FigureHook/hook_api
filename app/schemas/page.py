from __future__ import annotations

from math import ceil
from typing import Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import BaseModel, conint

T = TypeVar("T")


class PageParamsBase(Params):
    @property
    def skip(self):
        return (self.page - 1) * self.size


class PageInfo(BaseModel):
    page: conint(ge=1)  # type: ignore
    total_pages: conint(ge=1)  # type: ignore
    total_results: conint(ge=0)  # type: ignore


class Page(AbstractPage[T], Generic[T]):
    info: PageInfo
    results: Sequence[T]

    __params_type__ = PageParamsBase

    @classmethod
    def create(
        cls,
        results: Sequence[T],
        total_results: int,
        params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, PageParamsBase):
            raise ValueError("Page should be used with Params")

        info = PageInfo(
            page=params.page,
            total_pages=ceil(total_results / params.size) if total_results else 1,
            total_results=total_results,
        )

        return cls(
            info=info,
            results=results,
        )
