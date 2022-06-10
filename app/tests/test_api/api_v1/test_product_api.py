import random
from datetime import date, datetime

from app.core.config import settings
from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import \
    create_random_release_info_own_by_product
from deepdiff import DeepDiff
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

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


def v1_endpoint(path: str):
    return f"{settings.API_V1_ENDPOINT}{path}"


def test_get_products(client: TestClient, db: Session):
    for _ in range(random.randint(0, 200)):
        create_random_product(db)

    response = client.get(v1_endpoint("/products"))
    assert response.status_code == 200
    content = response.json()
    assert type(content) is list
    assert len(content) <= 100


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
        if key in rich_content:
            out_obj = content.get(key)
            struct = post_data.get(key)
            if type(out_obj) is list:
                for v in out_obj:
                    diff = DeepDiff(v, struct)
                    assert 'dictionary_item_added' not in diff
                    assert 'dictionary_item_removed' not in diff
            else:
                diff = DeepDiff(out_obj, struct)
                assert 'dictionary_item_added' not in diff
                assert 'dictionary_item_removed' not in diff

        if key not in rich_content:
            assert content.get(key) == post_data.get(key)


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
        if key in rich_content:
            out_obj = updated_product.get(key)
            struct = update_data.get(key)
            if type(out_obj) is list:
                for v in out_obj:
                    diff = DeepDiff(v, struct)
                    assert 'dictionary_item_added' not in diff
                    assert 'dictionary_item_removed' not in diff
            else:
                diff = DeepDiff(out_obj, struct)
                assert 'dictionary_item_added' not in diff
                assert 'dictionary_item_removed' not in diff

        if key not in rich_content:
            assert updated_product.get(key) == update_data.get(key)

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
