"""Add card reviews and review votes tables

Revision ID: add_card_reviews
Revises: add_merchants_table
Create Date: 2024-01-16 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'add_card_reviews'
down_revision = 'add_merchants_table'
branch_labels = None
depends_on = None

def upgrade():
    # Create card_reviews table
    op.create_table('card_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('card_master_id', sa.Integer(), nullable=False),
        sa.Column('overall_rating', sa.Integer(), nullable=False),
        sa.Column('review_title', sa.String(length=200), nullable=True),
        sa.Column('review_content', sa.Text(), nullable=True),
        sa.Column('pros', sa.Text(), nullable=True),
        sa.Column('cons', sa.Text(), nullable=True),
        sa.Column('experience', sa.Text(), nullable=True),
        sa.Column('is_verified_cardholder', sa.Boolean(), default=False),
        sa.Column('helpful_votes', sa.Integer(), default=0),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['card_master_id'], ['card_master_data.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'card_master_id', name='unique_user_card_review')
    )
    
    # Create review_votes table
    op.create_table('review_votes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('review_id', sa.Integer(), nullable=False),
        sa.Column('vote_type', sa.String(length=20), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['review_id'], ['card_reviews.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('user_id', 'review_id', name='unique_user_review_vote')
    )
    
    # Create indexes for better performance
    op.create_index('idx_card_reviews_card_id', 'card_reviews', ['card_master_id'])
    op.create_index('idx_card_reviews_user_id', 'card_reviews', ['user_id'])
    op.create_index('idx_card_reviews_rating', 'card_reviews', ['overall_rating'])
    op.create_index('idx_review_votes_review_id', 'review_votes', ['review_id'])
    op.create_index('idx_review_votes_user_id', 'review_votes', ['user_id'])

def downgrade():
    # Drop indexes
    op.drop_index('idx_review_votes_user_id', table_name='review_votes')
    op.drop_index('idx_review_votes_review_id', table_name='review_votes')
    op.drop_index('idx_card_reviews_rating', table_name='card_reviews')
    op.drop_index('idx_card_reviews_user_id', table_name='card_reviews')
    op.drop_index('idx_card_reviews_card_id', table_name='card_reviews')
    
    # Drop tables
    op.drop_table('review_votes')
    op.drop_table('card_reviews') 