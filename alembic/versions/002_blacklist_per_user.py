"""make token_blacklist unique per user

Revision ID: 002_blacklist_per_user
Revises: 001_initial_schema
Create Date: 2026-05-07
"""
from alembic import op
import sqlalchemy as sa

revision = '002_blacklist_per_user'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None

TABLE = 'token_blacklist'
OLD_COLUMNS = {'token_address', 'chain'}
NEW_CONSTRAINT = 'uq_token_blacklist_token_address_chain_added_by'
NEW_COLUMNS = ['token_address', 'chain', 'added_by']
RESTORED_CONSTRAINT = 'uq_token_blacklist_token_address_chain'


def _find_unique_constraint_names(bind, table, column_set):
    insp = sa.inspect(bind)
    names = []
    for uc in insp.get_unique_constraints(table):
        if set(uc['column_names']) == column_set:
            names.append(uc['name'])
    return names


def upgrade() -> None:
    bind = op.get_bind()
    old_names = _find_unique_constraint_names(bind, TABLE, OLD_COLUMNS)
    with op.batch_alter_table(TABLE) as batch_op:
        for name in old_names:
            batch_op.drop_constraint(name, type_='unique')
        batch_op.create_unique_constraint(NEW_CONSTRAINT, NEW_COLUMNS)


def downgrade() -> None:
    bind = op.get_bind()
    new_names = _find_unique_constraint_names(bind, TABLE, set(NEW_COLUMNS))
    with op.batch_alter_table(TABLE) as batch_op:
        for name in new_names:
            batch_op.drop_constraint(name, type_='unique')
        batch_op.create_unique_constraint(RESTORED_CONSTRAINT, list(OLD_COLUMNS))
