from __future__ import annotations

from math import ceil
from typing import Generic, Sequence, TypeVar

from fastapi_pagination import Params
from fastapi_pagination.bases import AbstractPage, AbstractParams
from pydantic import conint

T = TypeVar('T')


class Page(AbstractPage[T], Generic[T]):
    page: conint(ge=1)  # type: ignore
    total_pages: conint(ge=1)  # type: ignore
    total_results: conint(ge=0)  # type: ignore
    results: Sequence[T]

    __params_type__ = Params

    @classmethod
    def create(
            cls,
            results: Sequence[T],
            total_results: int,
            params: AbstractParams,
    ) -> Page[T]:
        if not isinstance(params, Params):
            raise ValueError("Page should be used with Params")

        return cls(
            page=params.page,
            total_pages=ceil(total_results / params.size),
            total_results=total_results,
            results=results,
        )
