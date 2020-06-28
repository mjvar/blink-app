"""empty message

Revision ID: ef32f692837e
Revises: 
Create Date: 2020-06-28 15:02:34.560402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ef32f692837e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('eye_data_entries')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('eye_data_entries',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('timestamp', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='eye_data_entries_pkey')
    )
    # ### end Alembic commands ###