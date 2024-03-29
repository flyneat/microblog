"""创建User、Instruction、PostFile表

Revision ID: fbd48c87f572
Revises: 
Create Date: 2019-12-16 17:16:01.760692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd48c87f572'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('telno', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('pwd_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_name'), 'user', ['name'], unique=True)
    op.create_index(op.f('ix_user_telno'), 'user', ['telno'], unique=True)
    op.create_table('instruction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sn', sa.String(length=20), nullable=True),
    sa.Column('content', sa.String(length=200), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_instruction_sn'), 'instruction', ['sn'], unique=False)
    op.create_index(op.f('ix_instruction_state'), 'instruction', ['state'], unique=False)
    op.create_index(op.f('ix_instruction_timestamp'), 'instruction', ['timestamp'], unique=False)
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('post_file',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=100), nullable=True),
                    sa.Column('type', sa.String(length=10), nullable=True),
                    sa.Column('length', sa.Integer(), nullable=True),
                    sa.Column('path', sa.String(length=1000), nullable=True),
                    sa.Column('uptime', sa.DateTime(), nullable=True),
                    sa.Column('sn', sa.String(length=20), nullable=True),
                    sa.Column('insts_id', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['insts_id'], ['instruction.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_index(op.f('ix_post_file_name'), 'post_file', ['name'], unique=False)
    op.create_index(op.f('ix_post_file_sn'), 'post_file', ['sn'], unique=False)
    op.create_index(op.f('ix_post_file_uptime'), 'post_file', ['uptime'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_post_file_uptime'), table_name='post_file')
    op.drop_index(op.f('ix_post_file_sn'), table_name='post_file')
    op.drop_index(op.f('ix_post_file_name'), table_name='post_file')
    op.drop_table('post_file')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_index(op.f('ix_instruction_timestamp'), table_name='instruction')
    op.drop_index(op.f('ix_instruction_state'), table_name='instruction')
    op.drop_index(op.f('ix_instruction_sn'), table_name='instruction')
    op.drop_table('instruction')
    op.drop_index(op.f('ix_user_telno'), table_name='user')
    op.drop_index(op.f('ix_user_name'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
