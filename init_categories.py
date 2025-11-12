#!/usr/bin/env python3
"""
Script para inicializar las categorías necesarias para el blog
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import BlogDatabase
from models import CategoryCreate

def init_categories():
    """Inicializa las categorías necesarias si no existen"""
    db = BlogDatabase()
    
    categories_to_create = [
        {
            "name": "Noticias",
            "slug": "noticias",
            "description": "Noticias sobre el ferrocarril en España"
        },
        {
            "name": "Curiosidades",
            "slug": "curiosidades",
            "description": "Curiosidades y datos interesantes sobre el ferrocarril"
        },
        {
            "name": "Eventos",
            "slug": "eventos",
            "description": "Eventos relacionados con el ferrocarril"
        }
    ]
    
    created_count = 0
    for cat_data in categories_to_create:
        # Check if category already exists
        existing = db.get_category_by_slug(cat_data["slug"])
        if not existing:
            category_data = CategoryCreate(
                name=cat_data["name"],
                slug=cat_data["slug"],
                description=cat_data["description"],
                parent_id=None
            )
            db.create_category(category_data)
            print(f"✓ Categoría '{cat_data['name']}' creada")
            created_count += 1
        else:
            print(f"○ Categoría '{cat_data['name']}' ya existe")
    
    print(f"\nTotal: {created_count} categorías creadas")
    return created_count

if __name__ == "__main__":
    init_categories()

