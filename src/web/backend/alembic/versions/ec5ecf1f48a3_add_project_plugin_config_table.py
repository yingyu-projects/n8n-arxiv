"""add_project_plugin_config_table

Revision ID: ec5ecf1f48a3
Revises: c121b49318b8
Create Date: 2025-01-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ec5ecf1f48a3'
down_revision = 'c121b49318b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database type
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    
    # Use appropriate types for each database
    id_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    fk_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    json_type = sa.JSON() if is_sqlite else postgresql.JSON
    
    # Check which tables already exist
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    # Create project_plugin_configs table
    if 'project_plugin_configs' not in existing_tables:
        op.create_table(
            'project_plugin_configs',
            sa.Column('id', id_type, primary_key=True),
            sa.Column('project_id', fk_type, sa.ForeignKey('projects.id'), nullable=False),
            sa.Column('plugin_id', fk_type, sa.ForeignKey('plugins.id'), nullable=False),
            sa.Column('config', json_type, nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.UniqueConstraint('project_id', 'plugin_id', name='uq_project_plugin'),
        )
        op.create_index('ix_project_plugin_configs_project_id', 'project_plugin_configs', ['project_id'])
        op.create_index('ix_project_plugin_configs_plugin_id', 'project_plugin_configs', ['plugin_id'])
    else:
        # Add indexes if they don't exist
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('project_plugin_configs')]
        if 'ix_project_plugin_configs_project_id' not in existing_indexes:
            op.create_index('ix_project_plugin_configs_project_id', 'project_plugin_configs', ['project_id'])
        if 'ix_project_plugin_configs_plugin_id' not in existing_indexes:
            op.create_index('ix_project_plugin_configs_plugin_id', 'project_plugin_configs', ['plugin_id'])


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    if 'project_plugin_configs' in existing_tables:
        # Drop indexes
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('project_plugin_configs')]
        if 'ix_project_plugin_configs_plugin_id' in existing_indexes:
            op.drop_index('ix_project_plugin_configs_plugin_id', table_name='project_plugin_configs')
        if 'ix_project_plugin_configs_project_id' in existing_indexes:
            op.drop_index('ix_project_plugin_configs_project_id', table_name='project_plugin_configs')
        
        # Drop unique constraint
        existing_constraints = [c['name'] for c in inspector.get_unique_constraints('project_plugin_configs')]
        if 'uq_project_plugin' in existing_constraints:
            op.drop_constraint('uq_project_plugin', 'project_plugin_configs', type_='unique')
        
        # Drop table
        op.drop_table('project_plugin_configs')

