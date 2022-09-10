import random
from datetime import date

import pytest
from app.models import (
    Category,
    Company,
    Paintwork,
    Product,
    ProductOfficialImage,
    ProductReleaseInfo,
    ReleaseTicket,
    Sculptor,
    Series,
)
from app.tests.utils.product import create_random_product
from app.tests.utils.release_info import create_random_release_info_own_by_product
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("db")
class TestRelationShip:
    def test_product_has_many_product_release_infos(self, db: Session):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 2, 12)
        )
        resale_info = ProductReleaseInfo(
            price=15800, initial_release_date=date(2021, 2, 12)
        )

        product.release_infos.extend([initial_info, resale_info])
        db.add(product)
        db.commit()

        fetched_product = db.get(Product, product.id)
        assert fetched_product
        assert isinstance(fetched_product.release_infos, list)
        assert len(fetched_product.release_infos) == 2
        assert fetched_product.release_infos[-1] == resale_info

    def test_fetech_product_last_product_release_infos(self, db):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 2, 12)
        )
        resale_info = ProductReleaseInfo(
            price=15800, initial_release_date=date(2021, 2, 12)
        )

        product.release_infos.extend([initial_info, resale_info])
        db.add(product)
        db.commit()

        f_p = db.get(Product, product.id)
        assert f_p
        last_release = f_p.last_release
        assert last_release == resale_info

    def test_product_release_infos_is_nullsfirst(self, db):
        product = Product(name="figure")
        initial_info = ProductReleaseInfo(
            price=12960, initial_release_date=date(2020, 2, 12)
        )
        resale_info = ProductReleaseInfo(
            price=15800, initial_release_date=date(2021, 2, 12)
        )
        stall_info = ProductReleaseInfo(price=16000)

        product.release_infos.extend([initial_info, resale_info, stall_info])
        db.add(product)
        db.commit()

        p = db.get(Product, product.id)
        assert p
        assert p.release_infos[0] == stall_info

    def test_series_has_many_products(self, db: Session):
        series = Series(name="foo")
        series.products.extend([Product(name="a"), Product(name="b")])
        products = series.products

        assert isinstance(products, list)
        assert len(products) == 2

    def test_company_has_many_products(self):
        company = Company(name="GSC")
        products = [Product(name="a"), Product(name="b")]
        company.released_products.extend(products)
        company.distributed_products.extend(products)
        company.made_products.extend(products)

        r_products = company.released_products
        m_products = company.made_products
        d_products = company.distributed_products

        assert isinstance(r_products, list)
        assert len(r_products) == 2

        assert isinstance(m_products, list)
        assert len(m_products) == 2

        assert isinstance(d_products, list)
        assert len(d_products) == 2

    def test_category_has_many_products(self):
        series = Category(name="figure")
        series.products.extend([Product(name="a"), Product(name="b")])

        assert isinstance(series.products, list)
        assert len(series.products) == 2

    def test_worker_has_many_products(self):
        paintwork = Paintwork(name="someone")
        sculptor = Sculptor(name="somebody")
        products = [Product(name="a"), Product(name="b")]

        paintwork.products.extend(products)
        sculptor.products.extend(products)

        assert isinstance(paintwork.products, list)
        assert len(paintwork.products) == 2
        assert isinstance(sculptor.products, list)
        assert len(sculptor.products) == 2

    def test_product_belongs_to_many_worker(self):
        product = Product(name="foo")

        p1 = Paintwork(name="p1")
        p2 = Paintwork(name="p2")

        s1 = Sculptor(name="s1")
        s2 = Sculptor(name="s2")

        product.sculptors.append(s1)
        product.sculptors.append(s2)
        product.paintworks.append(p1)
        product.paintworks.append(p2)

        assert isinstance(product.sculptors, list)
        assert len(product.sculptors) == 2
        assert isinstance(product.paintworks, list)
        assert len(product.paintworks) == 2

    def test_product_has_many_official_images(self):
        product = Product(name="foo")

        image_1 = ProductOfficialImage(url="http://foo.com/img1.jpg")
        image_2 = ProductOfficialImage(url="http://foo.com/img2.jpg")

        product.official_images.append(image_1)
        product.official_images.append(image_2)

        assert isinstance(product.official_images, list)
        assert len(product.official_images) == 2
        assert image_1.order == 1
        assert image_2.order == 2

    def test_images_would_be_deleted_when_product_was_deleted(self, db: Session):
        product = Product(name="foo")

        image_1 = ProductOfficialImage(url="http://foo.com/img1.jpg")
        image_2 = ProductOfficialImage(url="http://foo.com/img2.jpg")

        product.official_images.append(image_1)
        product.official_images.append(image_2)
        db.add(product)
        db.commit()
        db.delete(product)
        db.flush()

        assert not db.query(ProductOfficialImage).all()

    def test_release_info_would_be_deleted_when_product_was_deleted(self, db: Session):
        product = Product(name="foo")

        release_1 = ProductReleaseInfo(price=100)
        release_2 = ProductReleaseInfo(price=200)

        product.release_infos.append(release_1)
        product.release_infos.append(release_2)
        db.add(product)
        db.commit()

        db.delete(product)
        db.commit()

        assert not db.query(ProductReleaseInfo).all()

    def test_delete_product_and_association_but_not_effect_worker(self, db: Session):
        from app.models.relation_table import (
            product_paintwork_table,
            product_sculptor_table,
        )

        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        db.add(p)
        db.commit()

        db.delete(p)
        db.commit()

        s_asso = db.query(product_sculptor_table).all()
        p_asso = db.query(product_paintwork_table).all()
        assert not s_asso
        assert not p_asso
        assert db.query(Sculptor).all()
        assert db.query(Paintwork).all()

    def test_delete_paintwork_and_association_but_not_effect_product(self, db: Session):
        from app.models.relation_table import (
            product_paintwork_table,
            product_sculptor_table,
        )

        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        db.add(p)
        db.commit()

        db.delete(newbie)
        db.commit()

        s_asso = db.query(product_sculptor_table).all()
        p_asso = db.query(product_paintwork_table).all()
        assert s_asso
        assert not p_asso
        f_p = db.query(Product).first()
        assert f_p
        assert f_p.sculptors

    def test_delete_sculptor_and_association_but_not_affect_product(self, db: Session):
        from app.models.relation_table import (
            product_paintwork_table,
            product_sculptor_table,
        )

        p = Product(name="foo")
        master = Sculptor(name="master")
        newbie = Paintwork(name="newbie")

        p.paintworks.append(newbie)
        p.sculptors.append(master)
        db.add(p)
        db.commit()

        db.delete(master)
        db.commit()

        s_asso = db.query(product_sculptor_table).all()
        p_asso = db.query(product_paintwork_table).all()
        assert not s_asso
        assert p_asso

        f_p = db.query(Product).first()
        assert f_p
        assert not f_p.sculptors


@pytest.mark.usefixtures("db")
class TestReleaseFeedTicketRealtionShip:
    def test_delete_ticket_not_affect_release_info(self, db: Session):
        product = create_random_product(db)
        release_infos = [
            create_random_release_info_own_by_product(db, product_id=product.id)
            for _ in range(random.randint(1, 3))
        ]
        ticket = ReleaseTicket(release_infos=release_infos)
        db.add(ticket)
        db.commit()
        assert len(ticket.release_infos) == len(release_infos)

        db.delete(ticket)
        assert len(product.release_infos) == len(release_infos)

    def test_delete_release_info_not_affect_ticket(self, db: Session):
        product = create_random_product(db)
        release_infos = [
            create_random_release_info_own_by_product(db, product_id=product.id)
            for _ in range(random.randint(1, 3))
        ]
        ticket = ReleaseTicket(release_infos=release_infos)
        db.add(ticket)
        db.commit()
        db.delete(random.choice(release_infos))
        assert len(ticket.release_infos) == len(product.release_infos)
