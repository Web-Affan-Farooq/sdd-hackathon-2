"""Initial migration for Todo application."""

from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create todos table
    op.create_table(
        'todo',
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.Enum('pending', 'in_progress', 'completed', name='todostatus'), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index(op.f('ix_todo_user_id'), 'todo', ['user_id'], unique=False)
    op.create_index(op.f('ix_todo_created_at'), 'todo', ['created_at'], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f('ix_todo_created_at'), table_name='todo')
    op.drop_index(op.f('ix_todo_user_id'), table_name='todo')

    # Drop enum type
    op.execute("DROP TYPE IF EXISTS todostatus;")

    # Drop table
    op.drop_table('todo')