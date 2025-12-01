"""add_project_entity

Revision ID: c121b49318b8
Revises: 9a86870a2304
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'c121b49318b8'
down_revision = '9a86870a2304'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database type
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    
    # Use appropriate types for each database
    id_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    fk_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    
    # Check which tables already exist
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    # Create projects table
    if 'projects' not in existing_tables:
        op.create_table(
            'projects',
            sa.Column('id', id_type, primary_key=True),
            sa.Column('name', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
        )
        op.create_index('ix_projects_name', 'projects', ['name'])
    
    # Add project_id to workflows table (nullable initially for migration)
    if 'workflows' in existing_tables:
        # Check if column already exists
        existing_columns = [col['name'] for col in inspector.get_columns('workflows')]
        if 'project_id' not in existing_columns:
            if is_sqlite:
                # SQLite requires batch mode for adding columns with foreign keys
                with op.batch_alter_table('workflows', schema=None) as batch_op:
                    batch_op.add_column(sa.Column('project_id', fk_type, nullable=True))
                op.create_index('ix_workflows_project_id', 'workflows', ['project_id'])
            else:
                op.add_column('workflows', sa.Column('project_id', fk_type, sa.ForeignKey('projects.id'), nullable=True))
                op.create_index('ix_workflows_project_id', 'workflows', ['project_id'])
    
    # Add project_id to papers table (nullable initially for migration)
    if 'papers' in existing_tables:
        # Check if column already exists
        existing_columns = [col['name'] for col in inspector.get_columns('papers')]
        if 'project_id' not in existing_columns:
            if is_sqlite:
                # SQLite requires batch mode for adding columns with foreign keys
                with op.batch_alter_table('papers', schema=None) as batch_op:
                    batch_op.add_column(sa.Column('project_id', fk_type, nullable=True))
                op.create_index('ix_papers_project_id', 'papers', ['project_id'])
            else:
                op.add_column('papers', sa.Column('project_id', fk_type, sa.ForeignKey('projects.id'), nullable=True))
                op.create_index('ix_papers_project_id', 'papers', ['project_id'])


def downgrade() -> None:
    # Remove project_id from papers table
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    existing_tables = inspector.get_table_names()
    
    if 'papers' in existing_tables:
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('papers')]
        if 'ix_papers_project_id' in existing_indexes:
            op.drop_index('ix_papers_project_id', table_name='papers')
        existing_columns = [col['name'] for col in inspector.get_columns('papers')]
        if 'project_id' in existing_columns:
            op.drop_column('papers', 'project_id')
    
    # Remove project_id from workflows table
    if 'workflows' in existing_tables:
        existing_indexes = [idx['name'] for idx in inspector.get_indexes('workflows')]
        if 'ix_workflows_project_id' in existing_indexes:
            op.drop_index('ix_workflows_project_id', table_name='workflows')
        existing_columns = [col['name'] for col in inspector.get_columns('workflows')]
        if 'project_id' in existing_columns:
            op.drop_column('workflows', 'project_id')
    
    # Drop projects table
    if 'projects' in existing_tables:
        op.drop_index('ix_projects_name', table_name='projects')
        op.drop_table('projects')

