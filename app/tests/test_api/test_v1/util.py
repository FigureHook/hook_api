from typing import Any

from app.core.config import settings


def v1_endpoint(path: str):
    return f"{settings.API_V1_ENDPOINT}{path}"


def assert_pageination_content(
    content: Any,
    expected_page: int,
    expected_pages: int,
    total_results: int,
    results_size: int,
):
    assert "info" in content
    assert "results" in content

    info = content.get("info")
    results = content.get("results")

    assert "page" in info
    assert "total_pages" in info
    assert "total_results" in info
    assert info.get("page") == expected_page
    assert info.get("total_pages") == expected_pages
    assert info.get("total_results") == total_results

    assert type(results) is list
    assert len(results) <= results_size
