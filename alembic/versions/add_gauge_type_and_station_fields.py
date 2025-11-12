"""add gauge_type and station fields

Revision ID: add_gauge_station_fields
Revises: b43b6d995c9e
Create Date: 2024-12-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_gauge_station_fields'
down_revision = 'b43b6d995c9e'
branch_labels = None
depends_on = None


def upgrade():
    # Add gauge_type to lines table
    op.add_column('lines', sa.Column('gauge_type', sa.String(length=50), nullable=True))
    
    # Add station_type and province to stations table
    op.add_column('stations', sa.Column('station_type', sa.String(length=50), nullable=True))
    op.add_column('stations', sa.Column('province', sa.String(length=100), nullable=True))


def downgrade():
    # Remove columns
    op.drop_column('stations', 'province')
    op.drop_column('stations', 'station_type')
    op.drop_column('lines', 'gauge_type')

