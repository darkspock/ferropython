#!/bin/bash
# Script to run Alembic migration to add missing columns

echo "Running Alembic migration to add gauge_type and station fields..."
alembic upgrade head

echo "Migration completed!"

