"""Add merchants table for dynamic merchant management"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_merchants_table'
down_revision = 'add_card_master_data'
branch_labels = None
depends_on = None

def upgrade():
    # Create merchants table
    op.create_table('merchants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('merchant_name', sa.String(length=100), nullable=False),
        sa.Column('display_name', sa.String(length=100), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create index for faster lookups
    op.create_index('idx_merchant_name', 'merchants', ['merchant_name'])
    op.create_index('idx_merchant_category', 'merchants', ['category'])
    op.create_index('idx_merchant_active', 'merchants', ['is_active'])

def downgrade():
    op.drop_index('idx_merchant_active', table_name='merchants')
    op.drop_index('idx_merchant_category', table_name='merchants')
    op.drop_index('idx_merchant_name', table_name='merchants')
    op.drop_table('merchants') 