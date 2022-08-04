import random
from datetime import date, datetime
from math import ceil

from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import \
    create_random_release_info_own_by_product
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .util import assert_pageination_content, v1_endpoint

rich_content = {
    "series": {
        'id': 0,
        'name': 'name'
    },
    "category": {
        'id': 0,
        'name': 'name'
    },
    "manufacturer": {
        'id': 0,
        'name': 'name'
    },
    "releaser": {
        'id': 0,
        'name': 'name'
    },
    "distributer": {
        'id': 0,
        'name': 'name'
    },
    "sculptors": {
        'id': 0,
        'name': 'name'
    },
    "paintworks": {
        'id': 0,
        'name': 'name'
    },
    "official_images": {
        'id': 0,
        'order': 0,
        'url': 'url'
    }
}


def test_get_products(client: TestClient, db: Session):
    products_count = random.randint(0, 200)
    results_size = random.randint(1, 100)
    expected_pages = ceil(
        products_count / results_size
    ) if products_count else 1
    expected_page = random.randint(1, expected_pages)
    for _ in range(products_count):
        create_random_product(db)

    response = client.get(
        url=v1_endpoint("/products/"),
        params={
            'page': expected_page,
            'size': results_size
        }
    )
    assert response.status_code == 200

    content = response.json()
    assert_pageination_content(
        content,
        expected_page=expected_page,
        expected_pages=expected_pages,
        total_results=products_count,
        results_size=results_size
    )


def test_get_products_by_url(db: Session, client: TestClient):
    products_count = random.randint(0, 20)
    db_products = [
        create_random_product(db)
        for _ in range(products_count)
    ]
    choiced_product = random.choice(db_products)
    response = client.get(
        url=v1_endpoint("/products"),
        params={
            'source_url': choiced_product.url
        }
    )
    assert response.status_code == 200

    content = response.json()
    results = content.get('results')
    assert len(results) == 1, 'It should be at least one result.'
    assert results[0].get('url') == choiced_product.url


def test_create_product(client: TestClient, db: Session):
    post_data = {
        "name": "kappa",
        "size": 320,
        "scale": 7,
        "rerelease": False,
        "adult": True,
        "copyright": "By someone",
        "url": "https://company.com/581",
        "jan": "4580692150055",
        "id_by_official": "581",
        "checksum": "asdjk1290mfsddkljlhiijb3r",
        "order_period_start": datetime(2020, 2, 9, 9, 0, 0).isoformat(),
        "order_period_end": datetime(2020, 2, 15, 9, 0, 0).isoformat(),
        "series": "original foo",
        "category": "normal",
        "manufacturer": "good company",
        "releaser": "a b company",
        "distributer": "b company",
        "sculptors": [
            "master",
            "newbie"
        ],
        "paintworks": [
            "color",
            "grey"
        ],
        "official_images": [
            "/full/01.png",
            "/full/02.jpg"
        ]
    }

    response = client.post(
        v1_endpoint("/products/"),
        json=post_data
    )
    assert response.status_code == 201

    content = response.json()
    for key in post_data.keys():
        assert key in content


def test_get_product(client: TestClient, db: Session):
    check_keys = [
        'id',
        'name',
        'size',
        'rerelease',
        'adult',
        'copyright',
        'url',
        'jan',
        'checksum',
        'id_by_official',
        'order_period_start',
        'order_period_end',
        'created_at',
        'updated_at',
        'series',
        'category',
        'manufacturer',
        'releaser',
        'distributer',
        'sculptors',
        'paintworks',
        'official_images'
    ]

    product = create_random_product(db)
    response = client.get(
        v1_endpoint(f"/products/{product.id}")
    )
    fetched_product = response.json()
    assert response.status_code == 200
    for key in check_keys:
        assert key in fetched_product

    response = client.get(
        v1_endpoint("/products/5")
    )
    assert response.status_code == 404


def test_delete_product(db: Session, client: TestClient):
    product = create_random_product(db=db)
    response = client.delete(
        v1_endpoint(f"/products/{product.id}")
    )
    assert response.status_code == 204

    response = client.delete(
        v1_endpoint("/products/122")
    )
    assert response.status_code == 404


def test_update_product(db: Session, client: TestClient):
    product = create_random_product(db)
    update_data = {
        "name": "kappa",
        "size": 320,
        "scale": 7,
        "rerelease": False,
        "adult": True,
        "copyright": "By someone",
        "url": "https://company.com/581",
        "jan": "4580692150055",
        "id_by_official": "581",
        "checksum": "asdjk1290mfsddkljlhiijb3r",
        "order_period_start": datetime(2020, 2, 9, 9, 0, 0).isoformat(),
        "order_period_end": datetime(2020, 2, 15, 9, 0, 0).isoformat(),
        "series": "original foo",
        "category": "normal",
        "manufacturer": "good company",
        "releaser": "a b company",
        "distributer": "b company",
        "sculptors": [
            "master",
            "newbie"
        ],
        "paintworks": [
            "color",
            "grey"
        ],
        "official_images": [
            "/full/01.png",
            "/full/02.jpg"
        ]
    }
    response = client.put(
        v1_endpoint(f"/products/{product.id}"),
        json=update_data
    )
    assert response.status_code == 200

    updated_product = response.json()
    for key in update_data.keys():
        assert key in updated_product

    response = client.put(
        v1_endpoint("/products/1235"),
        json=update_data
    )
    assert response.status_code == 404


def test_create_product_release(db: Session, client: TestClient):
    product = create_random_product(db)
    release_data = {
        'price': 12700,
        'tax_including': False,
        'initial_release_date': date(2022, 5, 31).isoformat(),
        'announced_at': date(2021, 12, 28).isoformat(),
    }
    response = client.post(
        v1_endpoint(f"/products/{product.id}/release-infos"),
        json=release_data
    )
    assert response.status_code == 201

    content = response.json()
    assert content.get('product_id') == product.id
    for key in release_data:
        assert content.get(key) == release_data.get(key)

    response = client.post(
        v1_endpoint("/products/1325/release-infos"),
        json=release_data
    )
    assert response.status_code == 404


def test_get_product_releases(db: Session, client: TestClient):
    release_info_count = random.randint(0, 5)

    product = create_random_product(db)
    for _ in range(release_info_count):
        create_random_release_info_own_by_product(db, product_id=product.id)

    response = client.get(
        v1_endpoint(f"/products/{product.id}/release-infos"),
    )
    assert response.status_code == 200

    content = response.json()

    assert type(content) is list
    assert len(content) is release_info_count

    response = client.get(
        v1_endpoint("/products/123123/release-infos"),
    )
    assert response.status_code == 404


def test_get_product_images(db: Session, client: TestClient):
    product = create_random_product(db)
    response = client.get(v1_endpoint(
        f"/products/{product.id}/official-images"))
    assert response.status_code == 200

    content = response.json()
    assert type(content) is list
    assert len(content) == len(product.official_images)

    response = client.get(v1_endpoint(
        f"/products/12351235/official-images"))
    assert response.status_code == 404
