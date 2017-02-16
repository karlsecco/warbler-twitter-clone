"""empty message

Revision ID: 6fc7fc4ca974
Revises: ab14b79ab082
Create Date: 2017-02-16 12:05:09.169462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6fc7fc4ca974'
down_revision = 'ab14b79ab082'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('follows',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('followee_id', sa.Integer(), nullable=True),
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('follower_id != followee_id', name='no_self_follow'),
    sa.ForeignKeyConstraint(['followee_id'], ['users.id'], ondelete='cascade'),
    sa.ForeignKeyConstraint(['follower_id'], ['users.id'], ondelete='cascade'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('follows')
    # ### end Alembic commands ###