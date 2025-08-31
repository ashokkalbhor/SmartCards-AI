"""Add card master data tables for comparison

Revision ID: add_card_master_data
Revises: 
Create Date: 2024-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
# from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'add_card_master_data'
down_revision = None  # Update this with the latest revision
depends_on = None


def upgrade():
    # Create enum for card tiers
    card_tier_enum = sa.String(length=20)
    # card_tier_enum.create(op.get_bind())
    
    # Create card_master_data table
    op.create_table(
        'card_master_data',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bank_name', sa.String(length=100), nullable=False),
        sa.Column('card_name', sa.String(length=200), nullable=False),
        sa.Column('card_variant', sa.String(length=100), nullable=True),
        sa.Column('card_network', sa.String(length=50), nullable=False),
        sa.Column('card_tier', card_tier_enum, nullable=False),
        sa.Column('joining_fee', sa.Float(), nullable=True),
        sa.Column('annual_fee', sa.Float(), nullable=True),
        sa.Column('is_lifetime_free', sa.Boolean(), nullable=True),
        sa.Column('annual_fee_waiver_spend', sa.Float(), nullable=True),
        sa.Column('foreign_transaction_fee', sa.Float(), nullable=True),
        sa.Column('late_payment_fee', sa.Float(), nullable=True),
        sa.Column('overlimit_fee', sa.Float(), nullable=True),
        sa.Column('cash_advance_fee', sa.Float(), nullable=True),
        sa.Column('domestic_lounge_visits', sa.Integer(), nullable=True),
        sa.Column('international_lounge_visits', sa.Integer(), nullable=True),
        sa.Column('lounge_spend_requirement', sa.Float(), nullable=True),
        sa.Column('lounge_spend_period', sa.String(length=20), nullable=True),
        sa.Column('welcome_bonus_points', sa.Float(), nullable=True),
        sa.Column('welcome_bonus_spend_requirement', sa.Float(), nullable=True),
        sa.Column('welcome_bonus_timeframe', sa.Integer(), nullable=True),
        sa.Column('minimum_credit_limit', sa.Float(), nullable=True),
        sa.Column('maximum_credit_limit', sa.Float(), nullable=True),
        sa.Column('minimum_salary', sa.Float(), nullable=True),
        sa.Column('minimum_age', sa.Integer(), nullable=True),
        sa.Column('maximum_age', sa.Integer(), nullable=True),
        sa.Column('contactless_enabled', sa.Boolean(), nullable=True),
        sa.Column('chip_enabled', sa.Boolean(), nullable=True),
        sa.Column('mobile_wallet_support', sa.JSON(), nullable=True),
        sa.Column('insurance_benefits', sa.JSON(), nullable=True),
        sa.Column('concierge_service', sa.Boolean(), nullable=True),
        sa.Column('milestone_benefits', sa.JSON(), nullable=True),
        sa.Column('reward_program_name', sa.String(length=100), nullable=True),
        sa.Column('reward_expiry_period', sa.Integer(), nullable=True),
        sa.Column('reward_conversion_rate', sa.Float(), nullable=True),
        sa.Column('minimum_redemption_points', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('is_available_online', sa.Boolean(), nullable=True),
        sa.Column('launch_date', sa.DateTime(), nullable=True),
        sa.Column('discontinue_date', sa.DateTime(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('terms_and_conditions_url', sa.String(length=500), nullable=True),
        sa.Column('application_url', sa.String(length=500), nullable=True),
        sa.Column('additional_features', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_master_data_id'), 'card_master_data', ['id'], unique=False)
    op.create_index(op.f('ix_card_master_data_bank_name'), 'card_master_data', ['bank_name'], unique=False)

    # Create card_spending_categories table
    op.create_table(
        'card_spending_categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_master_id', sa.Integer(), nullable=False),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('category_display_name', sa.String(length=100), nullable=False),
        sa.Column('reward_rate', sa.Float(), nullable=False),
        sa.Column('reward_type', sa.String(length=50), nullable=True),
        sa.Column('reward_cap', sa.Float(), nullable=True),
        sa.Column('reward_cap_period', sa.String(length=20), nullable=True),
        sa.Column('minimum_transaction_amount', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('valid_from', sa.DateTime(), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('additional_conditions', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['card_master_id'], ['card_master_data.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_spending_categories_id'), 'card_spending_categories', ['id'], unique=False)

    # Create card_merchant_rewards table
    op.create_table(
        'card_merchant_rewards',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('card_master_id', sa.Integer(), nullable=False),
        sa.Column('merchant_name', sa.String(length=100), nullable=False),
        sa.Column('merchant_display_name', sa.String(length=100), nullable=False),
        sa.Column('merchant_category', sa.String(length=100), nullable=True),
        sa.Column('reward_rate', sa.Float(), nullable=False),
        sa.Column('reward_type', sa.String(length=50), nullable=True),
        sa.Column('reward_cap', sa.Float(), nullable=True),
        sa.Column('reward_cap_period', sa.String(length=20), nullable=True),
        sa.Column('minimum_transaction_amount', sa.Float(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('valid_from', sa.DateTime(), nullable=True),
        sa.Column('valid_until', sa.DateTime(), nullable=True),
        sa.Column('requires_registration', sa.Boolean(), nullable=True),
        sa.Column('additional_conditions', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['card_master_id'], ['card_master_data.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_card_merchant_rewards_id'), 'card_merchant_rewards', ['id'], unique=False)

    # Add foreign key to existing credit_cards table
    op.add_column('credit_cards', sa.Column('card_master_data_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'credit_cards', 'card_master_data', ['card_master_data_id'], ['id'])


def downgrade():
    # Remove foreign key from credit_cards table
    op.drop_constraint(None, 'credit_cards', type_='foreignkey')
    op.drop_column('credit_cards', 'card_master_data_id')
    
    # Drop tables
    op.drop_index(op.f('ix_card_merchant_rewards_id'), table_name='card_merchant_rewards')
    op.drop_table('card_merchant_rewards')
    
    op.drop_index(op.f('ix_card_spending_categories_id'), table_name='card_spending_categories')
    op.drop_table('card_spending_categories')
    
    op.drop_index(op.f('ix_card_master_data_bank_name'), table_name='card_master_data')
    op.drop_index(op.f('ix_card_master_data_id'), table_name='card_master_data')
    op.drop_table('card_master_data')
    
    # Drop enum
    card_tier_enum = sa.String(length=20)
    # card_tier_enum.drop(op.get_bind()) 