"""add reels table

Revision ID: add_reels_table
Revises: add_voices_table
Create Date: 2026-06-30 10:37:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_reels_table'
down_revision = 'add_voices_table'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'reels',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('project_id', sa.String(36), nullable=False),
        sa.Column('file_path', sa.String(512), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=True),
        sa.Column('format', sa.String(50), nullable=True),
        sa.Column('resolution', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('reels')
