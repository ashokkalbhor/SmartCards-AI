"""Add chat access control

Revision ID: 006
Revises: 005
Create Date: 2024-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


def upgrade():
    """Add chat access control fields and table"""
    # Add chat_access_granted field to users table
    op.add_column('users', sa.Column('chat_access_granted', sa.Boolean(), nullable=False, server_default='false'))
    
    # Create chat_access_requests table
    op.create_table(
        'chat_access_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='pending'),
        sa.Column('requested_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('reviewed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reviewed_by', sa.Integer(), nullable=True),
        sa.Column('review_notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['reviewed_by'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_chat_access_requests_id'), 'chat_access_requests', ['id'], unique=False)


def downgrade():
    """Remove chat access control fields and table"""
    # Drop chat_access_requests table
    op.drop_index(op.f('ix_chat_access_requests_id'), table_name='chat_access_requests')
    op.drop_table('chat_access_requests')
    
    # Remove chat_access_granted field from users table
    op.drop_column('users', 'chat_access_granted')
