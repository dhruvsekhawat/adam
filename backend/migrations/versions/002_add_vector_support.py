"""add vector support and document models

Revision ID: 002_add_vector_support
Revises: 001_create_users
Create Date: 2024-04-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_vector_support'
down_revision = '001_create_users'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Enable vector extension
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')
    
    # Create document_chunks table
    op.create_table(
        'document_chunks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('source_type', sa.String(), nullable=False),
        sa.Column('source_id', sa.String(), nullable=False),
        sa.Column('chunk_index', sa.Integer(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('chunk_metadata', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        # Use raw SQL for vector column
        sa.Column('embedding', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Alter the embedding column to be a vector
    op.execute('ALTER TABLE document_chunks ALTER COLUMN embedding TYPE vector(1536) USING embedding::vector(1536)')
    
    op.create_index(op.f('ix_document_chunks_id'), 'document_chunks', ['id'], unique=False)
    
    # Create email_metadata table
    op.create_table(
        'email_metadata',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('email_id', sa.String(), nullable=False),
        sa.Column('thread_id', sa.String(), nullable=True),
        sa.Column('subject', sa.String(), nullable=True),
        sa.Column('sender', sa.String(), nullable=True),
        sa.Column('recipients', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(), nullable=True),
        sa.Column('labels', postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column('is_processed', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_metadata_id'), 'email_metadata', ['id'], unique=False)
    op.create_index(op.f('ix_email_metadata_email_id'), 'email_metadata', ['email_id'], unique=True)
    
    # Add vector similarity index
    op.execute(
        'CREATE INDEX document_chunks_embedding_idx ON document_chunks USING ivfflat (embedding vector_l2_ops) WITH (lists = 100)'
    )

def downgrade() -> None:
    # Drop tables
    op.drop_table('document_chunks')
    op.drop_table('email_metadata')
    
    # Drop vector extension
    op.execute('DROP EXTENSION IF EXISTS vector') 