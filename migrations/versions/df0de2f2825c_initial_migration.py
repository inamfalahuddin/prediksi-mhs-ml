"""Initial migration.

Revision ID: df0de2f2825c
Revises: 
Create Date: 2024-06-14 01:17:35.514915

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'df0de2f2825c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(length=150), nullable=False),
                    sa.Column('email', sa.String(length=150), nullable=False),
                    sa.Column('password', sa.String(length=150), nullable=False),
                    sa.Column('role', sa.String(length=150), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('is_active', sa.Boolean(), default=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    sa.UniqueConstraint('username')
                    )

    op.create_table('mahasiswa',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('npm', sa.String(length=255), nullable=False, unique=True),
                    sa.Column('nama', sa.String(length=255)),
                    sa.Column('prodi', sa.String(length=255)),
                    sa.Column('tahun_masuk', sa.Integer(), nullable=True),
                    sa.Column('ket_aktif', sa.String(length=255), nullable=True, default='AKTIF'),
                    sa.Column('ket_lulus', sa.String(length=255), nullable=True, default='null'),
                    sa.Column('total_sks', sa.String(length=255), nullable=True, default='null'),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('npm'),
                    )

    op.create_table('transkip',
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('mahasiswa_id', sa.Integer, sa.ForeignKey('mahasiswa.id'), nullable=False, unique=False),
                    sa.Column('semester', sa.String(length=255), nullable=True),
                    sa.Column('ips', sa.Float(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    op.drop_table('mahasiswa')
    op.drop_table('transkip')
    # ### end Alembic commands ###
