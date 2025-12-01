"""add_plugin_system_tables

Revision ID: 9a86870a2304
Revises: b1f34b11a581
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '9a86870a2304'
down_revision = 'b1f34b11a581'
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
    
    # Create workflows table
    if 'workflows' not in existing_tables:
        op.create_table(
        'workflows',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('categories', json_type, nullable=False),
        sa.Column('num_papers', sa.Integer(), nullable=False, server_default='50'),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
        op.create_index('ix_workflows_name', 'workflows', ['name'], unique=True)
    elif 'ix_workflows_name' not in [idx['name'] for idx in inspector.get_indexes('workflows')]:
        op.create_index('ix_workflows_name', 'workflows', ['name'], unique=True)
    
    # Create plugins table
    if 'plugins' not in existing_tables:
        op.create_table(
        'plugins',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('version', sa.String(), nullable=False),
        sa.Column('config_schema', json_type, nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('plugin_metadata', json_type, nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
        op.create_index('ix_plugins_name', 'plugins', ['name'], unique=True)
    elif 'ix_plugins_name' not in [idx['name'] for idx in inspector.get_indexes('plugins')]:
        op.create_index('ix_plugins_name', 'plugins', ['name'], unique=True)
    
    # Create workflow_plugin_configs table
    # Include unique constraint in table creation for SQLite compatibility
    if 'workflow_plugin_configs' not in existing_tables:
        op.create_table(
        'workflow_plugin_configs',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('workflow_id', fk_type, sa.ForeignKey('workflows.id'), nullable=False),
        sa.Column('plugin_id', fk_type, sa.ForeignKey('plugins.id'), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('config', json_type, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.UniqueConstraint('workflow_id', 'plugin_id', name='uq_workflow_plugin'),
    )
        op.create_index('ix_workflow_plugin_configs_workflow_id', 'workflow_plugin_configs', ['workflow_id'])
        op.create_index('ix_workflow_plugin_configs_plugin_id', 'workflow_plugin_configs', ['plugin_id'])
    else:
        # Add indexes if they don't exist
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('workflow_plugin_configs')]
        if 'ix_workflow_plugin_configs_workflow_id' not in existing_indexes:
            op.create_index('ix_workflow_plugin_configs_workflow_id', 'workflow_plugin_configs', ['workflow_id'])
        if 'ix_workflow_plugin_configs_plugin_id' not in existing_indexes:
            op.create_index('ix_workflow_plugin_configs_plugin_id', 'workflow_plugin_configs', ['plugin_id'])
    
    # Create plugin_executions table
    if 'plugin_executions' not in existing_tables:
        op.create_table(
        'plugin_executions',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('plugin_id', fk_type, sa.ForeignKey('plugins.id'), nullable=False),
        sa.Column('workflow_id', fk_type, sa.ForeignKey('workflows.id'), nullable=False),
        sa.Column('workflow_run_id', sa.String(), nullable=False),
        sa.Column('paper_id', fk_type, sa.ForeignKey('papers.id'), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('config', json_type, nullable=False),
        sa.Column('result', json_type, nullable=True),
        sa.Column('started_at', sa.DateTime(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
    )
        op.create_index('ix_plugin_executions_plugin_id', 'plugin_executions', ['plugin_id'])
        op.create_index('ix_plugin_executions_workflow_id', 'plugin_executions', ['workflow_id'])
        op.create_index('ix_plugin_executions_workflow_run_id', 'plugin_executions', ['workflow_run_id'])
        op.create_index('ix_plugin_executions_paper_id', 'plugin_executions', ['paper_id'])


def downgrade() -> None:
    op.drop_index('ix_plugin_executions_paper_id', table_name='plugin_executions')
    op.drop_index('ix_plugin_executions_workflow_run_id', table_name='plugin_executions')
    op.drop_index('ix_plugin_executions_workflow_id', table_name='plugin_executions')
    op.drop_index('ix_plugin_executions_plugin_id', table_name='plugin_executions')
    op.drop_table('plugin_executions')
    
    op.drop_constraint('uq_workflow_plugin', 'workflow_plugin_configs', type_='unique')
    op.drop_index('ix_workflow_plugin_configs_plugin_id', table_name='workflow_plugin_configs')
    op.drop_index('ix_workflow_plugin_configs_workflow_id', table_name='workflow_plugin_configs')
    op.drop_table('workflow_plugin_configs')
    
    op.drop_index('ix_plugins_name', table_name='plugins')
    op.drop_table('plugins')
    
    op.drop_index('ix_workflows_name', table_name='workflows')
    op.drop_table('workflows')

