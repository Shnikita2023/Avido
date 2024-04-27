"""Initial tables

Revision ID: 68bb12c99f7a
Revises: 
Create Date: 2024-04-27 12:38:37.040161

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68bb12c99f7a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_code'), 'category', ['code'], unique=True)
    op.create_index(op.f('ix_category_id'), 'category', ['id'], unique=False)
    op.create_table('user',
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('middle_name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('role', sa.Enum('ADMIN', 'GUEST', 'USER', 'MODERATOR', name='role'), nullable=False),
    sa.Column('number_phone', sa.String(length=11), nullable=False),
    sa.Column('time_of_the_call', sa.String(length=50), nullable=False),
    sa.Column('status_user', sa.Enum('ACTIVE', 'BLOCKED', 'PENDING', name='statususer'), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_number_phone'), 'user', ['number_phone'], unique=True)
    op.create_table('advertisement',
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('city', sa.String(length=50), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('date_publication', sa.DateTime(timezone=True), nullable=False),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('number_of_views', sa.Integer(), nullable=False),
    sa.Column('photo', sa.String(), nullable=False),
    sa.Column('status_ad', sa.Enum('DRAFT', 'ON_MODERATION', 'REJECTED_FOR_REVISION', 'REMOVED', 'ACTIVE', name='statusad'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('category_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_advertisement_id'), 'advertisement', ['id'], unique=False)
    op.create_table('moderation',
    sa.Column('moderation_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('decision', sa.Enum('PUBLISH', 'MODIFICATION', name='decision'), nullable=False),
    sa.Column('rejection_reason', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('advertisement_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['advertisement_id'], ['advertisement.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('advertisement_id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_moderation_id'), 'moderation', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_moderation_id'), table_name='moderation')
    op.drop_table('moderation')
    op.drop_index(op.f('ix_advertisement_id'), table_name='advertisement')
    op.drop_table('advertisement')
    op.drop_index(op.f('ix_user_number_phone'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_category_id'), table_name='category')
    op.drop_index(op.f('ix_category_code'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###
