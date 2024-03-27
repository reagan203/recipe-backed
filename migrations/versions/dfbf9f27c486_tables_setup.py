"""tables setup

Revision ID: dfbf9f27c486
Revises: 
Create Date: 2024-03-27 10:52:30.802990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfbf9f27c486'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('gender', sa.Enum('male', 'female', 'other', name='gender'), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('recipe',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('instructions', sa.Text(), nullable=True),
    sa.Column('prep_time', sa.Integer(), nullable=True),
    sa.Column('cook_time', sa.Integer(), nullable=True),
    sa.Column('total_time', sa.Integer(), nullable=True),
    sa.Column('servings', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('recipe_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.recipe_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('rating',
    sa.Column('rating_id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.recipe_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('rating_id')
    )
    op.create_table('recipe_category',
    sa.Column('recipe_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.category_id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipe.recipe_id'], ),
    sa.PrimaryKeyConstraint('recipe_id', 'category_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recipe_category')
    op.drop_table('rating')
    op.drop_table('comment')
    op.drop_table('recipe')
    op.drop_table('user')
    op.drop_table('category')
    # ### end Alembic commands ###
