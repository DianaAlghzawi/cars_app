"""create table cars

Revision ID: 560049480135
Revises: b026be0193a7
Create Date: 2023-06-25 21:29:31.748233

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '560049480135'
down_revision = 'b026be0193a7'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('owner',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
                    sa.Column('first_name', sa.String(), nullable=False),
                    sa.Column('middle_name', sa.String(), nullable=True),
                    sa.Column('last_name', sa.String(), nullable=False),
                    sa.Column('national_number', sa.String(), nullable=False),
                    sa.Column('state', sa.String(), nullable=False),
                    sa.Column('zip', sa.String(), nullable=False),
                    sa.Column('gender', sa.String(), nullable=False),
                    sa.Column('birthdate', sa.DateTime(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.PrimaryKeyConstraint('id', name='owner_pk'),
                    sa.UniqueConstraint('national_number', name='national_number')
                    )
    op.create_table('cars',
                    sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
                    sa.Column('owner_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('brand', sa.String(), nullable=False),
                    sa.Column('year', sa.String(), nullable=False),
                    sa.Column('price', sa.Float(), nullable=False),
                    sa.Column('color', sa.String(), nullable=False),
                    sa.Column('vin', sa.String(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
                    sa.ForeignKeyConstraint(['owner_id'], ['owner.id'], ),
                    sa.PrimaryKeyConstraint('id', name='car_pk'),
                    sa.UniqueConstraint('vin', name='vin_key')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cars')
    op.drop_table('owner')
    # ### end Alembic commands ###
