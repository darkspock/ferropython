-- Script to manually fix posts table category column
-- Run this if the Alembic migration didn't complete correctly

-- Step 1: Add category column if it doesn't exist
ALTER TABLE posts ADD COLUMN IF NOT EXISTS category VARCHAR(50) NULL;

-- Step 2: Migrate data from category_id to category (if category_id exists)
UPDATE posts p
INNER JOIN categories c ON p.category_id = c.id
SET p.category = c.slug
WHERE c.slug IN ('noticias', 'curiosidades', 'eventos');

-- Step 3: Drop foreign key constraint (adjust constraint name as needed)
-- First, find the constraint name:
-- SELECT CONSTRAINT_NAME FROM information_schema.KEY_COLUMN_USAGE 
-- WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = 'posts' 
-- AND COLUMN_NAME = 'category_id' AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Then drop it (replace 'constraint_name' with actual name):
-- ALTER TABLE posts DROP FOREIGN KEY constraint_name;

-- Step 4: Drop category_id column
ALTER TABLE posts DROP COLUMN IF EXISTS category_id;

