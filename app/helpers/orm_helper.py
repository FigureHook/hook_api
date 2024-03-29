from typing import Sequence

from sqlalchemy import select
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import and_

from app.schemas.release_feed import ReleaseFeed
from app.models import (
    Company,
    Product,
    ProductOfficialImage,
    ProductReleaseInfo,
    Series,
)


class ReleaseFeedOrmHelper:
    @staticmethod
    def _make_statement(where_clause):
        """Release feed query statement maker."""
        stmt = (
            select(
                ProductReleaseInfo.id.label("release_info_id"),
                Product.id.label("product_id"),
                Product.name.label("name"),
                Product.url.label("source_url"),
                Product.adult.label("is_nsfw"),
                Product.rerelease.label("is_rerelease"),
                Series.name.label("series"),  # type: ignore
                Company.name.label("manufacturer"),  # type: ignore
                ProductReleaseInfo.price.label("price"),  # type: ignore
                ProductReleaseInfo.initial_release_date.label(
                    "release_date"
                ),  # type: ignore
                ProductOfficialImage.url.label("image_url"),  # type: ignore
                Product.og_image.label("og_image"),
                Product.size.label("size"),
                Product.scale.label("scale"),
            )
            .select_from(Product)
            .where(where_clause)
            .join(
                ProductReleaseInfo,
                ProductReleaseInfo.product_id == Product.id,
            )
            .join(Company, Company.id == Product.manufacturer_id)
            .join(Series, Series.id == Product.series_id, isouter=True)
            .join(
                ProductOfficialImage,
                and_(
                    Product.id == ProductOfficialImage.product_id,
                    ProductOfficialImage.order == 1,
                ),
            )
        )

        return stmt

    @staticmethod
    def fetch_release_feed_by_ids(
        session: Session, release_ids: Sequence[int]
    ) -> list[ReleaseFeed]:
        stmt = ReleaseFeedOrmHelper._make_statement(
            ProductReleaseInfo.id.in_(release_ids)
        )
        feeds = session.execute(stmt).all()

        release_feeds = []
        for feed in feeds:
            result = feed._asdict()
            release_feed = ReleaseFeed(
                product_id=result["product_id"],
                release_info_id=result["release_info_id"],
                name=result["name"],
                source_url=result["source_url"],
                is_nsfw=result["is_nsfw"],
                is_rerelease=result["is_rerelease"],
                series=result["series"],
                manufacturer=result["manufacturer"],
                size=result["size"],
                scale=result["scale"],
                price=result["price"],
                release_date=result["release_date"],
                image_url=result["og_image"] or result["image_url"],
                manufacturer_logo=None,
            )

            release_feeds.append(release_feed)

        return release_feeds
