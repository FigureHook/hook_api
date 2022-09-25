"""update

Revision ID: f29dd9c1b076
Revises: a37b35b25ceb
Create Date: 2022-09-23 17:44:04.147775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f29dd9c1b076'
down_revision = 'a37b35b25ceb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('release_ticket',
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('release_ticket_release_info_rel',
    sa.Column('ticket_id', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('release_info_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['release_info_id'], ['product_release_info.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ticket_id'], ['release_ticket.id'], ondelete='CASCADE')
    )
    op.add_column('application', sa.Column('last_seen_at', sa.DateTime(), nullable=True))
    op.drop_column('product', 'id_by_official')
    op.alter_column('product_official_image', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.add_column('webhook', sa.Column('currency', sa.String(length=3), nullable=True, comment='ISO 4217'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('webhook', 'currency')
    op.alter_column('product_official_image', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.add_column('product', sa.Column('id_by_official', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('application', 'last_seen_at')
    op.drop_table('release_ticket_release_info_rel')
    op.drop_table('release_ticket')
    # ### end Alembic commands ###