#!/usr/bin/env python3
"""Script to manually fix posts table: add category column and remove category_id"""
import os
from sqlalchemy import create_engine, text
from database import DATABASE_URL

def main():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Start a transaction
        trans = conn.begin()
        
        try:
            print("Step 1: Adding category column if it doesn't exist...")
            db_type = engine.dialect.name
            
            # Check if column exists first
            column_exists = False
            if db_type == 'mysql':
                result = conn.execute(text("""
                    SELECT COUNT(*) 
                    FROM information_schema.COLUMNS 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'posts' 
                    AND COLUMN_NAME = 'category'
                """))
                column_exists = result.scalar() > 0
            elif db_type == 'postgresql':
                result = conn.execute(text("""
                    SELECT COUNT(*) 
                    FROM information_schema.columns 
                    WHERE table_name = 'posts' 
                    AND column_name = 'category'
                """))
                column_exists = result.scalar() > 0
            elif db_type == 'sqlite':
                result = conn.execute(text("PRAGMA table_info(posts)"))
                column_exists = any(row[1] == 'category' for row in result)
            
            if not column_exists:
                try:
                    conn.execute(text("ALTER TABLE posts ADD COLUMN category VARCHAR(50) NULL"))
                    print("  ✓ Added category column")
                except Exception as e:
                    if "Duplicate column name" in str(e) or "already exists" in str(e).lower():
                        print("  ✓ Category column already exists")
                    else:
                        raise
            else:
                print("  ✓ Category column already exists")
            
            print("\nStep 2: Migrating data from category_id to category...")
            # Check database type
            db_type = engine.dialect.name
            
            if db_type == 'mysql':
                # MySQL syntax
                result = conn.execute(text("""
                    UPDATE posts p
                    INNER JOIN categories c ON p.category_id = c.id
                    SET p.category = c.slug
                    WHERE c.slug IN ('noticias', 'curiosidades', 'eventos')
                    AND (p.category IS NULL OR p.category = '')
                """))
            elif db_type == 'sqlite':
                # SQLite syntax (no table aliases in UPDATE)
                result = conn.execute(text("""
                    UPDATE posts
                    SET category = (
                        SELECT c.slug 
                        FROM categories c 
                        WHERE c.id = posts.category_id 
                        AND c.slug IN ('noticias', 'curiosidades', 'eventos')
                    )
                    WHERE category_id IN (
                        SELECT id FROM categories 
                        WHERE slug IN ('noticias', 'curiosidades', 'eventos')
                    )
                    AND (category IS NULL OR category = '')
                """))
            else:
                # PostgreSQL syntax
                result = conn.execute(text("""
                    UPDATE posts
                    SET category = c.slug
                    FROM categories c
                    WHERE posts.category_id = c.id
                    AND c.slug IN ('noticias', 'curiosidades', 'eventos')
                    AND (posts.category IS NULL OR posts.category = '')
                """))
            print(f"  ✓ Migrated {result.rowcount} posts")
            
            print("\nStep 3: Finding foreign key constraint...")
            db_type = engine.dialect.name
            
            if db_type == 'mysql':
                result = conn.execute(text("""
                    SELECT CONSTRAINT_NAME 
                    FROM information_schema.KEY_COLUMN_USAGE 
                    WHERE TABLE_SCHEMA = DATABASE() 
                    AND TABLE_NAME = 'posts' 
                    AND COLUMN_NAME = 'category_id' 
                    AND REFERENCED_TABLE_NAME IS NOT NULL
                """))
                constraints = [row[0] for row in result]
                
                if constraints:
                    for constraint_name in constraints:
                        print(f"  Dropping constraint: {constraint_name}")
                        conn.execute(text(f"ALTER TABLE posts DROP FOREIGN KEY {constraint_name}"))
                    print("  ✓ Dropped foreign key constraints")
                else:
                    print("  ✓ No foreign key constraints found (may have been dropped already)")
            elif db_type == 'postgresql':
                result = conn.execute(text("""
                    SELECT constraint_name
                    FROM information_schema.table_constraints
                    WHERE table_name = 'posts'
                    AND constraint_type = 'FOREIGN KEY'
                    AND constraint_name LIKE '%category_id%'
                """))
                constraints = [row[0] for row in result]
                
                if constraints:
                    for constraint_name in constraints:
                        print(f"  Dropping constraint: {constraint_name}")
                        conn.execute(text(f"ALTER TABLE posts DROP CONSTRAINT {constraint_name}"))
                    print("  ✓ Dropped foreign key constraints")
                else:
                    print("  ✓ No foreign key constraints found (may have been dropped already)")
            else:
                # SQLite doesn't enforce foreign keys the same way
                print("  ✓ Skipping foreign key constraint check (SQLite)")
            
            print("\nStep 4: Dropping category_id column...")
            try:
                conn.execute(text("ALTER TABLE posts DROP COLUMN category_id"))
                print("  ✓ Dropped category_id column")
            except Exception as e:
                if "doesn't exist" in str(e).lower() or "Unknown column" in str(e):
                    print("  ✓ Category_id column doesn't exist (may have been dropped already)")
                else:
                    raise
            
            # Commit the transaction
            trans.commit()
            print("\n✅ All changes applied successfully!")
            
        except Exception as e:
            trans.rollback()
            print(f"\n❌ Error: {e}")
            raise

if __name__ == "__main__":
    main()

