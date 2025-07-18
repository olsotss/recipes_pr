"""добавление таблиц

Revision ID: 0175f1463936
Revises: 9b4ad1d50f23
Create Date: 2025-07-15 16:24:15.605339

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '0175f1463936'
down_revision = '9b4ad1d50f23'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipes')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recipes',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('title', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('ingredients', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('steps', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('image', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('average_rating', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('recipes_pkey'))
    )
    # ### end Alembic commands ###
