"""added a relationship between the workout_exercises and units tables

Revision ID: bfddb2eaf5ef
Revises: 6d0c1ecbd723
Create Date: 2023-08-11 11:50:30.452626

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bfddb2eaf5ef"
down_revision = "6d0c1ecbd723"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "workout_exercises",
        sa.Column("unit_id", sa.Integer(), nullable=True),
    )
    op.create_foreign_key(None, "workout_exercises", "units", ["unit_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "workout_exercises", type_="foreignkey")
    op.drop_column("workout_exercises", "unit_id")
    # ### end Alembic commands ###