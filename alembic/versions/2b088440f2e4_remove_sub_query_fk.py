"""remove sub_query fk

Revision ID: 2b088440f2e4
Revises: 9e74d8969875
Create Date: 2022-11-04 09:52:34.453341

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2b088440f2e4'
down_revision = '9e74d8969875'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('adjustment_sub_query_guid_fkey', 'adjustment', type_='foreignkey')
    op.drop_column('adjustment', 'sub_query_guid')
    op.drop_constraint('apartment_sub_query_guid_fkey', 'apartment', type_='foreignkey')
    op.drop_column('apartment', 'sub_query_guid')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apartment', sa.Column('sub_query_guid', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('apartment_sub_query_guid_fkey', 'apartment', 'sub_query', ['sub_query_guid'], ['guid'])
    op.add_column('adjustment', sa.Column('sub_query_guid', postgresql.UUID(), autoincrement=False, nullable=False))
    op.create_foreign_key('adjustment_sub_query_guid_fkey', 'adjustment', 'sub_query', ['sub_query_guid'], ['guid'])
    # ### end Alembic commands ###