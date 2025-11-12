"""change_posts_category_id_to_category_enum

Revision ID: 0ba698cbecdb
Revises: da6d5fb2d56e
Create Date: 2025-01-27 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '0ba698cbecdb'
down_revision = 'da6d5fb2d56e'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add new category column (String) if it doesn't exist
    connection = op.get_bind()
    try:
        # Check if column already exists
        if connection.dialect.name == 'mysql':
            result = connection.execute(sa.text("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'posts' 
                AND COLUMN_NAME = 'category'
            """))
            column_exists = result.scalar() > 0
        else:
            # For other databases, try to add and catch error
            column_exists = False
        
        if not column_exists:
            op.add_column('posts', sa.Column('category', sa.String(length=50), nullable=True))
    except Exception:
        # If check fails, try to add column anyway
        try:
            op.add_column('posts', sa.Column('category', sa.String(length=50), nullable=True))
        except Exception:
            # Column might already exist, continue
            pass
    
    # Step 2: Migrate data from category_id to category (if category_id exists)
    # Map category IDs to enum values based on slug
    # This assumes categories table has slugs matching the enum values
    connection = op.get_bind()
    
    # Re-get connection after adding column
    if hasattr(connection, 'dialect') and connection.dialect.name == 'mysql':
        try:
            # Check if category_id column exists before trying to migrate
            result = connection.execute(sa.text("""
                SELECT COUNT(*) 
                FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'posts' 
                AND COLUMN_NAME = 'category_id'
            """))
            category_id_exists = result.scalar() > 0
        except:
            category_id_exists = False
    else:
        category_id_exists = True  # Assume it exists for other databases
    
    # Try to migrate existing data if categories table exists and category_id exists
    if category_id_exists:
        try:
            # Get category mappings
            result = connection.execute(sa.text("""
                SELECT c.id, c.slug 
                FROM categories c
                WHERE c.slug IN ('noticias', 'curiosidades', 'eventos')
            """))
            category_map = {row[0]: row[1] for row in result}
            
            # Update posts with category based on category_id
            for cat_id, cat_slug in category_map.items():
                connection.execute(sa.text("""
                    UPDATE posts 
                    SET category = :slug 
                    WHERE category_id = :cat_id AND (category IS NULL OR category = '')
                """), {"slug": cat_slug, "cat_id": cat_id})
            connection.commit()
        except Exception as e:
            # If categories table doesn't exist or migration fails, just leave category as NULL
            import logging
            logging.warning(f"Could not migrate category data: {e}")
            pass
    
    # Step 3: Drop foreign key constraint and column (if they exist)
    try:
        # For SQLite, we need to recreate the table
        if op.get_bind().dialect.name == 'sqlite':
            # SQLite doesn't support dropping columns directly, so we'll use a workaround
            # Create a new table without category_id
            op.create_table('posts_new',
                sa.Column('id', sa.Integer(), nullable=False),
                sa.Column('title', sa.String(length=255), nullable=False),
                sa.Column('content', sa.Text(), nullable=False),
                sa.Column('author', sa.String(length=100), nullable=False),
                sa.Column('is_published', sa.Boolean(), nullable=True),
                sa.Column('category', sa.String(length=50), nullable=True),
                sa.Column('created_at', sa.DateTime(), nullable=True),
                sa.Column('updated_at', sa.DateTime(), nullable=True),
            )
            
            # Copy data
            op.execute("""
                INSERT INTO posts_new (id, title, content, author, is_published, category, created_at, updated_at)
                SELECT id, title, content, author, is_published, category, created_at, updated_at
                FROM posts
            """)
            
            # Drop old table and rename new one
            op.drop_table('posts')
            op.rename_table('posts_new', 'posts')
            op.create_primary_key('pk_posts', 'posts', ['id'])
        else:
            # For MySQL, PostgreSQL, etc.
            # First, try to find and drop the foreign key constraint
            # MySQL foreign key names can vary, so we'll try common patterns
            connection = op.get_bind()
            try:
                # Get foreign key constraint name
                if op.get_bind().dialect.name == 'mysql':
                    result = connection.execute(sa.text("""
                        SELECT CONSTRAINT_NAME 
                        FROM information_schema.KEY_COLUMN_USAGE 
                        WHERE TABLE_SCHEMA = DATABASE() 
                        AND TABLE_NAME = 'posts' 
                        AND COLUMN_NAME = 'category_id' 
                        AND REFERENCED_TABLE_NAME IS NOT NULL
                    """))
                    constraints = [row[0] for row in result]
                    for constraint_name in constraints:
                        op.drop_constraint(constraint_name, 'posts', type_='foreignkey')
                else:
                    # PostgreSQL
                    op.drop_constraint('fk_posts_category_id', 'posts', type_='foreignkey')
            except Exception:
                # Try common constraint names
                for constraint_name in ['fk_posts_category_id', 'posts_ibfk_1', 'posts_category_id_fkey']:
                    try:
                        op.drop_constraint(constraint_name, 'posts', type_='foreignkey')
                        break
                    except Exception:
                        continue
            
            # Drop the category_id column
            op.drop_column('posts', 'category_id')
    except Exception as e:
        # If constraint doesn't exist or column doesn't exist, continue
        # Log the error but don't fail
        import logging
        logging.warning(f"Could not drop category_id: {e}")
        pass


def downgrade():
    # Step 1: Add category_id column back
    op.add_column('posts', sa.Column('category_id', sa.Integer(), nullable=True))
    
    # Step 2: Try to restore category_id from category slug
    connection = op.get_bind()
    try:
        # Get category mappings
        result = connection.execute(sa.text("""
            SELECT c.id, c.slug 
            FROM categories c
            WHERE c.slug IN ('noticias', 'curiosidades', 'eventos')
        """))
        category_map = {row[1]: row[0] for row in result}
        
        # Update posts with category_id based on category slug
        for cat_slug, cat_id in category_map.items():
            connection.execute(sa.text(f"""
                UPDATE posts 
                SET category_id = :cat_id 
                WHERE category = :slug
            """), {"cat_id": cat_id, "slug": cat_slug})
    except Exception:
        pass
    
    # Step 3: Recreate foreign key constraint
    try:
        op.create_foreign_key('posts_ibfk_1', 'posts', 'categories', ['category_id'], ['id'])
    except Exception:
        pass
    
    # Step 4: Drop category column
    if op.get_bind().dialect.name == 'sqlite':
        # SQLite workaround: recreate table
        op.create_table('posts_new',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(length=255), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('author', sa.String(length=100), nullable=False),
            sa.Column('is_published', sa.Boolean(), nullable=True),
            sa.Column('category_id', sa.Integer(), nullable=True),
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.Column('updated_at', sa.DateTime(), nullable=True),
        )
        
        op.execute("""
            INSERT INTO posts_new (id, title, content, author, is_published, category_id, created_at, updated_at)
            SELECT id, title, content, author, is_published, category_id, created_at, updated_at
            FROM posts
        """)
        
        op.drop_table('posts')
        op.rename_table('posts_new', 'posts')
        op.create_primary_key('pk_posts', 'posts', ['id'])
    else:
        op.drop_column('posts', 'category')
