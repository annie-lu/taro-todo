"""create accounts table

Revision ID: 0e5667d0a75a
Revises:
Create Date: 2020-11-21 14:34:53.082760

"""
import sqlalchemy as db
from alembic import op

# revision identifiers, used by Alembic.
revision = '9b1d3dcf21f9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    account = op.create_table(
        'account',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('username', db.String(60), index=True, unique=True),
    db.Column('password_hash', db.String(128))
    )

    tasks = op.create_table(
        'tasks',
    db.Column('id', db.Integer, index=True,primary_key=True, autoincrement=True),
    db.Column('content', db.Text, index=True,nullable=False),
    db.Column('done', db.Boolean, index=True,default=False),
      db.Column('account_id', db.Integer,db.ForeignKey('account.id'),nullable=False),
    db.Column('completed_at', db.DateTime),
        db.Column('deleted_at', db.DateTime)

    )

    pets = op.create_table(
        'pets',
        db.Column('id',db.Integer, index=True,primary_key=True, autoincrement=True),
        db.Column('type',db.Text,nullable=False),
        db.Column('health',db.Float, index=True),
        db.Column('points',db.Integer, index=True),
        db.Column('account_id', db.Integer, db.ForeignKey('account.id'), nullable=False)
    )

def downgrade():
    op.drop_table('account')
    op.drop_table('tasks')
    op.drop_table('pets')
