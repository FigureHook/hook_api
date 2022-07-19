from typing import Any

from app.core.config import settings


def v1_endpoint(path: str):
    return f"{settings.API_V1_ENDPOINT}{path}"


def assert_pageination_content(
    content: Any,
    expected_page: int,
    expected_pages: int,
    total_results: int,
    results_size: int
):
    assert 'page' in content
    assert 'total_pages' in content
    assert 'total_results' in content
    assert 'results' in content

    assert content.get('page') == expected_page
    assert content.get('total_pages') == expected_pages
    assert content.get('total_results') == total_results

    assert type(content['results']) is list
    assert len(content['results']) <= results_size
