"""Add card master data tables for comparison

Revision ID: 001_add_card_master_data
Revises: 
Create Date: 2024-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_add_card_master_data'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create card_master_data table
    op.create_table('card_master_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_name', sa.String(length=100), nullable=False),
        sa.Column('bank_name', sa.String(length=100), nullable=False),
        sa.Column('card_tier', sa.String(length=50), nullable=False),
        sa.Column('annual_fee', sa.Float(), nullable=True),
        sa.Column('joining_fee', sa.Float(), nullable=True),
        sa.Column('reward_rate_general', sa.Float(), nullable=True),
        sa.Column('reward_rate_online_shopping', sa.Float(), nullable=True),
        sa.Column('reward_rate_dining', sa.Float(), nullable=True),
        sa.Column('reward_rate_travel', sa.Float(), nullable=True),
        sa.Column('reward_rate_fuel', sa.Float(), nullable=True),
        sa.Column('reward_rate_entertainment', sa.Float(), nullable=True),
        sa.Column('reward_rate_groceries', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index('idx_card_master_bank', 'card_master_data', ['bank_name'])
    op.create_index('idx_card_master_tier', 'card_master_data', ['card_tier'])
    op.create_index('idx_card_master_active', 'card_master_data', ['is_active'])

    # Create card_spending_categories table
    op.create_table('card_spending_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('reward_rate', sa.Float(), nullable=False),
        sa.Column('monthly_cap', sa.Float(), nullable=True),
        sa.Column('annual_cap', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['card_master_data.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create card_merchant_rewards table
    op.create_table('card_merchant_rewards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_id', sa.Integer(), nullable=False),
        sa.Column('merchant_name', sa.String(length=100), nullable=False),
        sa.Column('reward_rate', sa.Float(), nullable=False),
        sa.Column('monthly_cap', sa.Float(), nullable=True),
        sa.Column('annual_cap', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['card_id'], ['card_master_data.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('card_merchant_rewards')
    op.drop_table('card_spending_categories')
    op.drop_index('idx_card_master_active', table_name='card_master_data')
    op.drop_index('idx_card_master_tier', table_name='card_master_data')
    op.drop_index('idx_card_master_bank', table_name='card_master_data')
    op.drop_table('card_master_data') 