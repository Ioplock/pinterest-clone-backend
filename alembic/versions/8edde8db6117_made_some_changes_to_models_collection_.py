"""Made some changes to models (collection_association added pin_id and collection_id)

Revision ID: 8edde8db6117
Revises: 9508e2ef5b88
Create Date: 2025-01-01 02:42:13.543071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8edde8db6117'
down_revision: Union[str, None] = '9508e2ef5b88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pins')
    op.drop_table('pin_collection_associations')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_index('ix_users_username', table_name='users')
    op.drop_table('users')
    op.drop_table('file_types')
    op.drop_table('pin_collections')
    op.drop_table('pin_tags')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pin_tags',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=32), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pin_collections',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('file_types',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=8), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('username', sa.VARCHAR(length=32), nullable=False),
    sa.Column('display_name', sa.VARCHAR(length=32), nullable=True),
    sa.Column('email', sa.VARCHAR(length=64), nullable=False),
    sa.Column('hashed_password', sa.VARCHAR(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_users_username', 'users', ['username'], unique=1)
    op.create_index('ix_users_email', 'users', ['email'], unique=1)
    op.create_table('pin_collection_associations',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('added_to_collection_timestamp', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('order_number', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pins',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=128), nullable=False),
    sa.Column('description', sa.VARCHAR(length=512), nullable=True),
    sa.Column('owner_id', sa.INTEGER(), nullable=False),
    sa.Column('upload_timestamp', sa.DATETIME(), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.Column('type_id', sa.INTEGER(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['file_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
