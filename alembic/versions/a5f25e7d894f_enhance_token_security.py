"""enhance token security

Revision ID: a5f25e7d894f
Revises: 25ce89045453
Create Date: 2021-11-28 08:31:38.641913

"""
import sqlalchemy as sa
from alembic import op
from app.helpers.encrypt_helper import EncryptHelper
from app.models import Webhook

# revision identifiers, used by Alembic.
revision = "a5f25e7d894f"
down_revision = "25ce89045453"
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    webhooks = session.execute(f"SELECT id, token FROM webhook;")
    # webhooks = session.query(Webhook).all()

    for w in webhooks:
        session.execute(
            f"UPDATE webhook SET token='{EncryptHelper.encrypt(w.token)}' WHERE id='{w.id}';"
        )

    session.add_all(webhooks)
    session.commit()
    session.close()


def downgrade():
    bind = op.get_bind()
    session = sa.orm.Session(bind=bind)

    webhooks = session.execute(f"SELECT id, token FROM webhook;")
    for w in webhooks:
        session.execute(
            f"UPDATE {Webhook.__tablename__} SET token='{EncryptHelper.decrypt(w.token)}' WHERE id='{w.id}';"
        )
    session.commit()
    session.close()
