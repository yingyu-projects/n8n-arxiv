"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Detect database type
    bind = op.get_bind()
    is_sqlite = bind.dialect.name == 'sqlite'
    
    # Use appropriate types for each database
    id_type = sa.String() if is_sqlite else postgresql.UUID(as_uuid=True)
    json_type = sa.JSON() if is_sqlite else postgresql.JSON
    
    # Create papers table
    op.create_table(
        'papers',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('pdf_link', sa.String(), nullable=False),
        sa.Column('arxiv_id', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('summary', json_type, nullable=True),
        sa.Column('parsed_at', sa.DateTime(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('ix_papers_pdf_link', 'papers', ['pdf_link'], unique=True)
    
    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', id_type, primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('num_papers', sa.Integer(), nullable=False, server_default='0'),
    )
    op.create_index('ix_categories_name', 'categories', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index('ix_categories_name', table_name='categories')
    op.drop_table('categories')
    op.drop_index('ix_papers_pdf_link', table_name='papers')
    op.drop_table('papers')

