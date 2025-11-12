-- Manual fix for posts table: add category column and remove category_id
-- Execute this directly in MySQL if the Alembic migration didn't work

-- Step 1: Add category column if it doesn't exist
ALTER TABLE posts ADD COLUMN category VARCHAR(50) NULL;

-- Step 2: Migrate data from category_id to category
UPDATE posts p
INNER JOIN categories c ON p.category_id = c.id
SET p.category = c.slug
WHERE c.slug IN ('noticias', 'curiosidades', 'eventos')
AND p.category IS NULL;

-- Step 3: Find and drop foreign key constraint
-- First, find the constraint name (run this separately to get the name):
-- SELECT CONSTRAINT_NAME 
-- FROM information_schema.KEY_COLUMN_USAGE 
-- WHERE TABLE_SCHEMA = DATABASE() 
-- AND TABLE_NAME = 'posts' 
-- AND COLUMN_NAME = 'category_id' 
-- AND REFERENCED_TABLE_NAME IS NOT NULL;

-- Then drop it (replace 'YOUR_CONSTRAINT_NAME' with the actual name from above):
-- ALTER TABLE posts DROP FOREIGN KEY YOUR_CONSTRAINT_NAME;

-- Step 4: Drop category_id column
ALTER TABLE posts DROP COLUMN category_id;

