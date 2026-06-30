"""add voices table

Revision ID: add_voices_table
Revises: add_images_table
Create Date: 2026-06-30 01:35:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_voices_table'
down_revision = 'add_images_table'
branch_labels = None
depends_on = None


def upgrade():
    # Create voices table
    op.create_table(
        'voices',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('scene_id', sa.String(36), sa.ForeignKey('scenes.id'), nullable=False),
        sa.Column('project_id', sa.String(36), sa.ForeignKey('projects.id'), nullable=False),
        sa.Column('file_path', sa.String(512), nullable=False),
        sa.Column('voice_used', sa.String(100), nullable=False),
        sa.Column('text_used', sa.String(2000), nullable=False),
        sa.Column('duration', sa.String(50), nullable=True),
        sa.Column('is_approved', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False)
    )


def downgrade():
    op.drop_table('voices')
