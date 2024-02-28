"""Test

Revision ID: fa518dd00df6
Revises: 
Create Date: 2023-12-16 03:04:02.336500

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fa518dd00df6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('articles')
    with op.batch_alter_table('chat_history', schema=None) as batch_op:
        batch_op.add_column(sa.Column('chat_name', sa.String(length=40), nullable=False))
        batch_op.create_foreign_key(None, 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('chat_history', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_column('chat_name')

    op.create_table('articles',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('titles', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('body', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
