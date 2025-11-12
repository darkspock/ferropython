"""
Script to populate Spanish cities in the database
"""

import json
from database import BlogDatabase, CityModel
from models import CityCreate

# 20 major Spanish cities for the railway blog
SPANISH_CITIES = [
    {"name": "Madrid", "slug": "madrid", "region": "Comunidad de Madrid"},
    {"name": "Barcelona", "slug": "barcelona", "region": "Cataluña"},
    {"name": "Valencia", "slug": "valencia", "region": "Comunidad Valenciana"},
    {"name": "Sevilla", "slug": "sevilla", "region": "Andalucía"},
    {"name": "Bilbao", "slug": "bilbao", "region": "País Vasco"},
    {"name": "Málaga", "slug": "malaga", "region": "Andalucía"},
    {"name": "Zaragoza", "slug": "zaragoza", "region": "Aragón"},
    {"name": "Murcia", "slug": "murcia", "region": "Región de Murcia"},
    {"name": "Palma", "slug": "palma", "region": "Islas Baleares"},
    {"name": "Las Palmas", "slug": "las-palmas", "region": "Islas Canarias"},
    {"name": "Alicante", "slug": "alicante", "region": "Comunidad Valenciana"},
    {"name": "Córdoba", "slug": "cordoba", "region": "Andalucía"},
    {"name": "Valladolid", "slug": "valladolid", "region": "Castilla y León"},
    {"name": "Vigo", "slug": "vigo", "region": "Galicia"},
    {"name": "Gijón", "slug": "gijon", "region": "Asturias"},
    {"name": "Vitoria", "slug": "vitoria", "region": "País Vasco"},
    {"name": "A Coruña", "slug": "a-coruna", "region": "Galicia"},
    {"name": "Granada", "slug": "granada", "region": "Andalucía"},
    {"name": "Elche", "slug": "elche", "region": "Comunidad Valenciana"},
    {"name": "Oviedo", "slug": "oviedo", "region": "Asturias"},
]


def populate_cities():
    """Populate the database with Spanish cities"""
    db = BlogDatabase()
    session = db.get_db()

    try:
        # Check if cities already exist
        existing_cities = session.query(CityModel).count()
        if existing_cities > 0:
            print(
                f"Found {existing_cities} cities already in database. Skipping population."
            )
            return

        # Add cities
        for city_data in SPANISH_CITIES:
            city = CityModel(
                name=city_data["name"],
                slug=city_data["slug"],
                region=city_data["region"],
                country="Spain",
            )
            session.add(city)

        session.commit()
        print(
            f"Successfully added {len(SPANISH_CITIES)} Spanish cities to the database."
        )

        # Display added cities
        for city in SPANISH_CITIES:
            print(f"  - {city['name']} ({city['region']})")

    except Exception as e:
        session.rollback()
        print(f"Error populating cities: {e}")
    finally:
        session.close()


if __name__ == "__main__":
    populate_cities()
