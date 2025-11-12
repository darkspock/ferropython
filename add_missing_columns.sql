-- SQL script to add missing columns to lines and stations tables
-- Run this manually if Alembic migration doesn't work

-- Add gauge_type to lines table
ALTER TABLE `lines` ADD COLUMN `gauge_type` VARCHAR(50) NULL AFTER `status`;

-- Add station_type and province to stations table
ALTER TABLE `stations` ADD COLUMN `station_type` VARCHAR(50) NULL AFTER `accessibility`;
ALTER TABLE `stations` ADD COLUMN `province` VARCHAR(100) NULL AFTER `station_type`;

