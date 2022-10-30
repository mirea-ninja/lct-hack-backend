"""add query, archive tables

Revision ID: 4465ac864230
Revises: c9a642144513
Create Date: 2022-10-30 14:48:57.551593

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '4465ac864230'
down_revision = 'c9a642144513'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('archive',
    sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('created_by', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('input_file', sa.String(), nullable=False),
    sa.Column('output_file', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_archive_guid'), 'archive', ['guid'], unique=True)
    op.create_table('query',
    sa.Column('guid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('archive_guid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['archive_guid'], ['archive.guid'], ),
    sa.PrimaryKeyConstraint('guid')
    )
    op.create_index(op.f('ix_query_guid'), 'query', ['guid'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_query_guid'), table_name='query')
    op.drop_table('query')
    op.drop_index(op.f('ix_archive_guid'), table_name='archive')
    op.drop_table('archive')
    # ### end Alembic commands ###