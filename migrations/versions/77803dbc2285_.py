"""empty message

Revision ID: 77803dbc2285
Revises: 1d4c18f8f404
Create Date: 2016-09-02 21:13:58.411028

"""

# revision identifiers, used by Alembic.
revision = '77803dbc2285'
down_revision = '1d4c18f8f404'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('message', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    ### end Alembic commands ###
