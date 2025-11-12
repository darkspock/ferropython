"""add_category_id_to_posts

Revision ID: da6d5fb2d56e
Revises: add_gauge_station_fields
Create Date: 2025-11-12 14:25:08.425234

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da6d5fb2d56e'
down_revision: Union[str, None] = 'add_gauge_station_fields'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add category_id column to posts table
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'fk_posts_category_id',
        'posts', 'categories',
        ['category_id'], ['id']
    )


def downgrade() -> None:
    # Remove category_id column from posts table
    op.drop_constraint('fk_posts_category_id', 'posts', type_='foreignkey')
    op.drop_column('posts', 'category_id')
