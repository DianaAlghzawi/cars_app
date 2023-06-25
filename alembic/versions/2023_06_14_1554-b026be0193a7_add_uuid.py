"""Add uuid

Revision ID: b026be0193a7
Revises:
Create Date: 2023-06-14 15:54:21.064218

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'b026be0193a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
