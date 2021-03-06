"""empty message

Revision ID: 665b5c690659
Revises: 3e5c36615577
Create Date: 2016-09-02 21:53:33.061872

"""

# revision identifiers, used by Alembic.
revision = '665b5c690659'
down_revision = '3e5c36615577'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('rendered_message', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'rendered_message')
    ### end Alembic commands ###
