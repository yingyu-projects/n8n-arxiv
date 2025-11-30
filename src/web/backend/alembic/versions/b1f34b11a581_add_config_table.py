"""add_config_table

Revision ID: b1f34b11a581
Revises: 001
Create Date: 2025-11-30 23:48:26.432693

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'b1f34b11a581'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database type
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    
    # Use appropriate types for each database
    id_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    
    # Create configs table
    op.create_table(
        'configs',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('key', sa.String(), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
    )
    op.create_index('ix_configs_key', 'configs', ['key'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_configs_key', table_name='configs')
    op.drop_table('configs')

