"""make token_blacklist unique per user

Revision ID: 002_blacklist_per_user
Revises: 001_initial_schema
Create Date: 2026-05-07
"""
from alembic import op

revision = '002_blacklist_per_user'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table('token_blacklist') as batch_op:
        batch_op.drop_constraint('uq_token_blacklist_token_address_chain', type_='unique')
        batch_op.create_unique_constraint(
            'uq_token_blacklist_token_address_chain_added_by',
            ['token_address', 'chain', 'added_by'],
        )


def downgrade() -> None:
    with op.batch_alter_table('token_blacklist') as batch_op:
        batch_op.drop_constraint('uq_token_blacklist_token_address_chain_added_by', type_='unique')
        batch_op.create_unique_constraint(
            'uq_token_blacklist_token_address_chain',
            ['token_address', 'chain'],
        )
