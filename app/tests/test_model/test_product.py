from datetime import date, datetime

import pytest
from app.models import Product, ProductOfficialImage, ProductReleaseInfo
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestProduct:
    def test_created_at_default_is_datetime(self, db: Session):
        product = Product(name="foo")
        db.add(product)
        db.commit()

        assert bool(product.created_at)
        assert isinstance(product.created_at, datetime)

    def test_checksum_comparison(self):
        checksum = "111"
        product = Product(
            name="foo figure", url="www.foo.com", checksum="111")

        assert product.check_checksum(checksum)


@pytest.mark.usefixtures("db")
class TestProductReleaseInfo:
    def test_basic_info_adjust_release_date(self):
        p = Product(name="foo")
        info_has_init_date = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id
        )
        delay_date = date(2021, 1, 1)

        info_has_init_date.adjust_release_date_to(delay_date)
        assert info_has_init_date.adjusted_release_date == delay_date

        delay_datetime = datetime(2022, 2, 2, 12)

        info_has_init_date.adjust_release_date_to(delay_datetime)
        assert info_has_init_date.adjusted_release_date == delay_datetime.date()

        with pytest.raises(AssertionError):
            info_has_init_date.adjust_release_date_to(1)  # type: ignore

    def test_stall_info_adjust_release_date(self):
        p = Product(name="foo")
        stall_info = ProductReleaseInfo(price=12960, product_id=p.id)
        delay_date = date(2021, 1, 1)

        stall_info.adjust_release_date_to(delay_date)
        assert stall_info.initial_release_date == delay_date

    def test_release_date_could_be_brought_forward(self):
        p = Product(name="foo")
        init_date = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id
        )

        early_date = date(2019, 12, 1)
        init_date.adjust_release_date_to(early_date)

        assert init_date.initial_release_date == date(2020, 1, 1)
        assert init_date.adjusted_release_date == early_date

    def test_stall_release(self):
        p = Product(name="foo")
        info = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id)
        info.stall()
        assert not info.initial_release_date

    def test_get_release_date(self):
        p = Product(name="foo")
        info_1 = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 1, 1), product_id=p.id)
        assert info_1.release_date == date(2020, 1, 1)

        info_2 = ProductReleaseInfo(price=12960, initial_release_date=date(2020, 1, 1),
                                    adjusted_release_date=date(2020, 5, 1), product_id=p.id)
        assert info_2.release_date == date(2020, 5, 1)

        info_3 = ProductReleaseInfo(price=12960, product_id=p.id)
        assert info_3.release_date == None


@pytest.mark.usefixtures("db")
class TestProductImage:
    def test_image_list_process(self, db: Session):
        urls = ["https://img.com/001.jpg", "https://image.net/17nb123f75.png"]

        images = ProductOfficialImage.create_image_list(urls)

        assert len(images) == len(urls)
        for image in images:
            assert image.url in urls
