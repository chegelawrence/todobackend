"""empty message

Revision ID: a285dbc51e7e
Revises: 
Create Date: 2019-07-24 14:12:53.931282

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a285dbc51e7e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'todos', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'todos', type_='foreignkey')
    op.drop_column('todos', 'user_id')
    # ### end Alembic commands ###
