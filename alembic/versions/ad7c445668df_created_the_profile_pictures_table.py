"""created the profile_pictures table

Revision ID: ad7c445668df
Revises: 9cf5aa27a548
Create Date: 2023-08-26 11:52:07.055740

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ad7c445668df'
down_revision = '9cf5aa27a548'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profile_pictures',
    sa.Column('url', sa.TEXT(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['profile_id'], ['profiles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('profiles', 'profile_picture')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('profiles', sa.Column('profile_picture', postgresql.BYTEA(), autoincrement=False, nullable=True))
    op.drop_table('profile_pictures')
    # ### end Alembic commands ###