"""Initial database setup

Revision ID: f5fb392e6b0a
Revises:
Create Date: 2024-04-22 15:11:16.001681

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f5fb392e6b0a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    conn = op.get_bind()
    op.create_table(
        "pipelines",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("is_deleted", sa.Boolean(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("custom_data", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "chat_history",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("message_role", sa.String(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=False),
        sa.Column("pipeline_id", sa.UUID(), nullable=True),
        sa.Column("session_id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipelines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    op.create_table(
        "pipeline_configurations",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("pipeline_id", sa.UUID(), nullable=True),
        sa.Column(
            "config_type",
            sa.Enum(
                "INPUT_SOURCE",
                "EMBEDDING_MODEL",
                "INFERENCE_MODEL",
                "OUTPUT_SOURCE",
                "TRACE_DETAILS",
                "PII_FILTER",
                "SUMMARIZER",
                name="configtype",
                create_constraint=True,
            ),
            nullable=False,
        ),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("config", sa.JSON(), nullable=True),
        sa.Column("custom_data", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["pipeline_id"],
            ["pipelines.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
    )
    if not conn.dialect.has_type(conn, "configtype"):
        op.execute(
            "CREATE TYPE configtype AS ENUM('INPUT_SOURCE', 'EMBEDDING_MODEL', 'INFERENCE_MODEL', 'OUTPUT_SOURCE', 'TRACE_DETAILS', 'PII_FILTER', 'SUMMARIZER')"
        )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("pipeline_configurations")
    op.drop_table("chat_history")
    op.drop_table("pipelines")
    op.execute("DROP TYPE IF EXISTS configtype")
    # ### end Alembic commands ###
