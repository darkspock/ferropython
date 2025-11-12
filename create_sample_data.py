#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos de prueba realistas
para el blog de transporte ferroviario.
"""

import sys
import os
from datetime import datetime, timedelta
from random import choice, randint
from sqlalchemy.orm import Session

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal
from database import (
    PostModel,
    PageModel,
    LineModel,
    StationModel,
    ProjectModel,
    EventModel,
    CityModel,
    CategoryModel,
)


def create_sample_data():
    """Crear datos de muestra para todas las tablas"""

    # Create database tables
    from database import Base

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # 1. Crear Ciudades
        print("Creando ciudades...")
        cities_data = [
            {
                "name": "Buenos Aires",
                "slug": "buenos-aires",
                "region": "Metropolitana",
                "country": "Argentina",
            },
            {
                "name": "Rosario",
                "slug": "rosario",
                "region": "Litoral",
                "country": "Argentina",
            },
            {
                "name": "Córdoba",
                "slug": "cordoba",
                "region": "Centro",
                "country": "Argentina",
            },
            {
                "name": "Mendoza",
                "slug": "mendoza",
                "region": "Cuyo",
                "country": "Argentina",
            },
            {
                "name": "La Plata",
                "slug": "la-plata",
                "region": "Buenos Aires",
                "country": "Argentina",
            },
            {
                "name": "Mar del Plata",
                "slug": "mar-del-plata",
                "region": "Buenos Aires",
                "country": "Argentina",
            },
        ]

        cities = []
        for city_data in cities_data:
            city = CityModel(
                name=city_data["name"],
                slug=city_data["slug"],
                region=city_data["region"],
                country=city_data["country"],
                created_at=datetime.now() - timedelta(days=randint(30, 365)),
                updated_at=datetime.now(),
            )
            cities.append(city)
            db.add(city)

        db.commit()

        # 2. Crear Categorías
        print("Creando categorías...")
        categories_data = [
            {
                "name": "Infraestructura",
                "slug": "infraestructura",
                "description": "Noticias sobre vías, estaciones y equipamiento",
            },
            {
                "name": "Trenes",
                "slug": "trenes",
                "description": "Información sobre locomotoras y material rodante",
            },
            {
                "name": "Modernización",
                "slug": "modernizacion",
                "description": "Proyectos de mejora y actualización",
            },
            {
                "name": "Servicios",
                "slug": "servicios",
                "description": "Noticias sobre servicios de pasajeros y carga",
            },
            {
                "name": "Seguridad",
                "slug": "seguridad",
                "description": "Artículos sobre seguridad ferroviaria",
            },
            {
                "name": "Historia",
                "slug": "historia",
                "description": "Contenido histórico del ferrocarril",
            },
        ]

        categories = []
        for cat_data in categories_data:
            category = CategoryModel(
                name=cat_data["name"],
                slug=cat_data["slug"],
                description=cat_data["description"],
                created_at=datetime.now() - timedelta(days=randint(30, 365)),
                updated_at=datetime.now(),
            )
            categories.append(category)
            db.add(category)

        db.commit()

        # 3. Crear Líneas
        print("Creando líneas ferroviarias...")
        lines_data = [
            {
                "line_number": "LG-MITRE",
                "description": "Conecta Buenos Aires con Rosario, Córdoba y Tucumán",
                "status": "active",
                "cities_served": ["Buenos Aires", "Rosario", "Córdoba", "Tucumán"],
            },
            {
                "line_number": "LG-ROCA",
                "description": "Cubre el sur del Gran Buenos Aires y destinos marítimos",
                "status": "active",
                "cities_served": [
                    "Buenos Aires",
                    "La Plata",
                    "Mar del Plata",
                    "Bahía Blanca",
                ],
            },
            {
                "line_number": "LG-SANMARTIN",
                "description": "Une Buenos Aires con el oeste del país",
                "status": "active",
                "cities_served": ["Buenos Aires", "Mendoza", "San Juan"],
            },
            {
                "line_number": "LG-URQUIZA",
                "description": "Conecta Buenos Aires con Entre Ríos y Mesopotamia",
                "status": "active",
                "cities_served": ["Buenos Aires", "Paraná", "Concepción del Uruguay"],
            },
            {
                "line_number": "LG-BELGRANO",
                "description": "Principal red de transporte de cargas del país",
                "status": "active",
                "cities_served": [
                    "Buenos Aires",
                    "Rosario",
                    "Córdoba",
                    "Salta",
                    "Jujuy",
                ],
            },
        ]

        lines = []
        for line_data in lines_data:
            line = LineModel(
                line_number=line_data["line_number"],
                description=line_data["description"],
                status=line_data["status"],
                cities_served=",".join(line_data["cities_served"]),
                created_at=datetime.now() - timedelta(days=randint(60, 365)),
                updated_at=datetime.now(),
            )
            lines.append(line)
            db.add(line)

        db.commit()

        # 4. Crear Estaciones
        print("Creando estaciones...")
        stations_data = [
            {
                "station_code": "RTI",
                "name": "Retiro Mitre",
                "address": "Av. Ramos Mejía 1508, Buenos Aires",
                "city_id": cities[0].id,
                "services": ["Venta de pasajes", "Guarda equipajes", "Restaurante"],
                "accessibility": ["Rampa", "Ascensor", "Baños adaptados"],
            },
            {
                "station_code": "TIG",
                "name": "Tigre",
                "address": "Av. Liniers 200, Tigre",
                "city_id": cities[0].id,
                "services": ["Venta de pasajes", "Cafetería"],
                "accessibility": ["Rampa"],
            },
            {
                "station_code": "RSN",
                "name": "Rosario Norte",
                "address": "Av. Ovidio Lagos 1500, Rosario",
                "city_id": cities[1].id,
                "services": ["Venta de pasajes", "Estacionamiento", "Restaurante"],
                "accessibility": ["Rampa", "Ascensor"],
            },
            {
                "station_code": "CBA",
                "name": "Córdoba",
                "address": "Av. General Paz 450, Córdoba",
                "city_id": cities[2].id,
                "services": ["Venta de pasajes", "Guarda equipajes", "Estacionamiento"],
                "accessibility": ["Rampa", "Ascensor", "Baños adaptados"],
            },
            {
                "station_code": "CON",
                "name": "Constitución",
                "address": "Av. Brasil 500, Buenos Aires",
                "city_id": cities[0].id,
                "services": ["Venta de pasajes", "Subte conexión", "Comercios"],
                "accessibility": ["Rampa", "Ascensor"],
            },
            {
                "station_code": "LPT",
                "name": "La Plata",
                "address": "Calle 1 y 50, La Plata",
                "city_id": cities[4].id,
                "services": ["Venta de pasajes", "Estacionamiento"],
                "accessibility": ["Rampa"],
            },
            {
                "station_code": "MDP",
                "name": "Mar del Plata",
                "address": "Av. Luro 2500, Mar del Plata",
                "city_id": cities[5].id,
                "services": ["Venta de pasajes", "Guarda equipajes", "Restaurante"],
                "accessibility": ["Rampa", "Ascensor"],
            },
            {
                "station_code": "OCS",
                "name": "Once",
                "address": "Av. Pueyrredón 600, Buenos Aires",
                "city_id": cities[0].id,
                "services": ["Venta de pasajes", "Subte conexión", "Comercios"],
                "accessibility": ["Rampa"],
            },
            {
                "station_code": "MDZ",
                "name": "Mendoza",
                "address": "Av. España 1000, Mendoza",
                "city_id": cities[3].id,
                "services": ["Venta de pasajes", "Estacionamiento"],
                "accessibility": ["Rampa", "Ascensor"],
            },
            {
                "station_code": "FLC",
                "name": "Federico Lacroze",
                "address": "Av. Federico Lacroze 1000, Buenos Aires",
                "city_id": cities[0].id,
                "services": ["Venta de pasajes", "Subte conexión"],
                "accessibility": ["Rampa", "Ascensor"],
            },
        ]

        stations = []
        for station_data in stations_data:
            station = StationModel(
                station_code=station_data["station_code"],
                name=station_data["name"],
                address=station_data["address"],
                city_id=station_data["city_id"],
                services=",".join(station_data["services"]),
                accessibility=",".join(station_data["accessibility"]),
                created_at=datetime.now() - timedelta(days=randint(30, 365)),
                updated_at=datetime.now(),
            )
            stations.append(station)
            db.add(station)

        db.commit()

        # 5. Crear Posts
        print("Creando posts del blog...")
        posts_content = [
            {
                "title": "Modernización del Corredor Ferroviario Central",
                "content": """El Gobierno Nacional anunció una inversión histórica de $500 millones para la modernización del corredor ferroviario central que conecta Buenos Aires con Rosario y Córdoba.

El proyecto incluye la renovación de 300 km de vías, la instalación de nuevos sistemas de señalización y la adquisición de material rodante moderno. Se estima que estas obras mejorarán la velocidad comercial en un 40% y aumentarán la capacidad de transporte en un 60%.

Las obras comenzarán en el primer trimestre del próximo año y tendrán una duración estimada de 24 meses. Durante el período de construcción, se garantizará el servicio mínimo en todos los tramos.""",
                "is_published": True,
            },
            {
                "title": "Nuevos Trenes Eléctricos para el Servicio Suburbano",
                "content": """Llegaron al país los primeros 20 trenes eléctricos modernos que reemplazarán a las formaciones antiguas en las líneas suburbanas de Buenos Aires.

Los nuevos trenes cuentan con aire acondicionado, sistema de información para pasajeros, acceso para personas con movilidad reducida y sistemas de seguridad avanzados. Cada formación tiene capacidad para 1200 pasajeros y alcanza una velocidad máxima de 120 km/h.

La incorporación de estos trenes permitirá reducir los tiempos de viaje en un 25% y aumentar la frecuencia de los servicios durante las horas pico.""",
                "is_published": True,
            },
            {
                "title": "Inauguración del Nuevo Centro de Control de Tráfico",
                "content": """Fue inaugurado hoy el nuevo Centro de Control de Tráfico Ferroviario más moderno de América Latina. La instalación, ubicada en Buenos Aires, monitorea en tiempo real más de 10.000 km de vías.

El centro cuenta con tecnología de punta que permite optimizar el tráfico ferroviario, prevenir incidentes y coordinar mejor los servicios de pasajeros y cargas. Se espera que la nueva tecnología reduzca los retrasos en un 35%.

El proyecto demandó una inversión de $80 millones y fue ejecutado en colaboración con especialistas ferroviarios de Europa y Japón.""",
                "is_published": True,
            },
            {
                "title": "Record Histórico en Transporte de Cargas",
                "content": """El sistema ferroviario de cargas transportó el año pasado 25 millones de toneladas, marcando un récord histórico para la última década.

El crecimiento fue impulsado principalmente por el aumento en el transporte de granos, minerales y contenedores. La línea Belgrano Cargas fue la que mayor volumen movió, con el 45% del total.

Este resultado refleja la recuperación del modo ferroviario como alternativa eficiente y sustentable para el transporte de mercancías a largas distancias.""",
                "is_published": True,
            },
            {
                "title": "Plan de Seguridad Ferroviaria 2024-2028",
                "content": """Se presentó el Plan Nacional de Seguridad Ferroviaria que contempla una inversión de $200 millones en los próximos cinco años.

El plan incluye la instalación de sistemas de detección de obstáculos, modernización de pasos a nivel, capacitación del personal y mejoras en la señalización. Se espera reducir los incidentes en un 50% durante el período de implementación.

Además, se crearán programas de concientización vial en las comunidades cercanas a las vías para promover una cultura de seguridad ferroviaria.""",
                "is_published": True,
            },
        ]

        posts = []
        for i, post_data in enumerate(posts_content):
            post = PostModel(
                title=post_data["title"],
                content=post_data["content"],
                author="Administrador del Blog",
                is_published=post_data["is_published"],
                created_at=datetime.now() - timedelta(days=i * 5, hours=randint(1, 23)),
                updated_at=datetime.now() - timedelta(days=i * 2, hours=randint(1, 23)),
            )
            posts.append(post)
            db.add(post)

        db.commit()

        # 6. Crear Páginas
        print("Creando páginas estáticas...")
        pages_data = [
            {
                "title": "Sobre el Blog",
                "slug": "sobre",
                "content": """Bienvenidos al Blog Ferroviario, un espacio dedicado a compartir noticias, historias y análisis sobre el mundo del transporte ferroviario en Argentina y América Latina.

Nuestra misión es difundir la importancia del ferrocarril como modo de transporte sustentable, eficiente y estratégico para el desarrollo económico y social de nuestros países.

En este espacio encontrarán:
- Noticias actualizadas sobre proyectos ferroviarios
- Artículos técnicos sobre infraestructura y material rodante
- Historias y anécdotas de la rica historia ferroviaria
- Análisis sobre políticas de transporte
- Entrevistas con expertos del sector

El blog es mantenido por un equipo de apasionados del ferrocarril con amplia experiencia en el sector.""",
                "is_published": True,
            },
            {
                "title": "Contacto",
                "slug": "contacto",
                "content": """¿Querés contactarte con nosotros?

Podés escribirnos a:
- Email: info@blogferroviario.com
- Twitter: @blogferroviario
- Instagram: @blog_ferroviario

Nos interesa conocer tu opinión, sugerencias o propuestas para mejorar el contenido del blog. Si tenés alguna noticia ferroviaria que quieras compartir, también nos podés contactar.

Para consultas comerciales o publicitarias, por favor especificar en el asunto del correo.

¡Gracias por seguirnos!""",
                "is_published": True,
            },
        ]

        pages = []
        for page_data in pages_data:
            page = PageModel(
                title=page_data["title"],
                slug=page_data["slug"],
                content=page_data["content"],
                is_published=page_data["is_published"],
                created_at=datetime.now() - timedelta(days=randint(30, 60)),
                updated_at=datetime.now(),
            )
            pages.append(page)
            db.add(page)

        db.commit()

        # 7. Crear Proyectos
        print("Creando proyectos...")
        projects_data = [
            {
                "title": "Renovación Vía Mitre-Rosario",
                "description": "Modernización completa del corredor Buenos Aires-Rosario",
                "project_type": "Infraestructura",
                "status": "En Ejecución",
                "budget": 500000000,
                "timeline": "24 meses",
                "category_id": categories[2].id,  # Modernización
                "city_id": cities[0].id,
            },
            {
                "title": "Electrificación Línea San Martín",
                "description": "Proyecto de electrificación del tramo suburbano",
                "project_type": "Electrificación",
                "status": "En Planificación",
                "budget": 800000000,
                "timeline": "36 meses",
                "category_id": categories[2].id,  # Modernización
                "city_id": cities[0].id,
            },
            {
                "title": "Nuevo Taller Ferroviario Córdoba",
                "description": "Construcción de taller moderno para mantenimiento de trenes",
                "project_type": "Construcción",
                "status": "En Ejecución",
                "budget": 120000000,
                "timeline": "12 meses",
                "category_id": categories[0].id,  # Infraestructura
                "city_id": cities[2].id,
            },
        ]

        projects = []
        for project_data in projects_data:
            project = ProjectModel(
                title=project_data["title"],
                description=project_data["description"],
                project_type=project_data["project_type"],
                status=project_data["status"],
                budget=project_data["budget"],
                timeline=project_data["timeline"],
                category_id=project_data["category_id"],
                city_id=project_data["city_id"],
                created_at=datetime.now() - timedelta(days=randint(30, 180)),
                updated_at=datetime.now(),
            )
            projects.append(project)
            db.add(project)

        db.commit()

        # 8. Crear Eventos
        print("Creando eventos...")
        events_data = [
            {
                "title": "Exposición Ferroviaria Internacional",
                "description": "La más grande exposición de material rodante y tecnología ferroviaria de América Latina",
                "event_type": "Exposición",
                "event_date": datetime.now() + timedelta(days=45),
                "location": "Centro de Exposiciones, Buenos Aires",
                "city_id": cities[0].id,
            },
            {
                "title": "Jornadas de Seguridad Ferroviaria",
                "description": "Congreso internacional sobre mejores prácticas en seguridad ferroviaria",
                "event_type": "Congreso",
                "event_date": datetime.now() + timedelta(days=30),
                "location": "Universidad Tecnológica Nacional",
                "city_id": cities[0].id,
            },
            {
                "title": "Tren Histórico del Centenario",
                "description": "Viaje especial en tren histórico conmemorativo",
                "event_type": "Evento Especial",
                "event_date": datetime.now() + timedelta(days=60),
                "location": "Estación Retiro - Estación Tigre",
                "city_id": cities[0].id,
            },
        ]

        events = []
        for event_data in events_data:
            event = EventModel(
                title=event_data["title"],
                description=event_data["description"],
                event_type=event_data["event_type"],
                event_date=event_data["event_date"],
                location=event_data["location"],
                city_id=event_data["city_id"],
                created_at=datetime.now() - timedelta(days=randint(15, 60)),
                updated_at=datetime.now(),
            )
            events.append(event)
            db.add(event)

        db.commit()

        print("\n✅ Datos de prueba creados exitosamente!")
        print(f"📊 Resumen:")
        print(f"   • Ciudades: {len(cities)}")
        print(f"   • Categorías: {len(categories)}")
        print(f"   • Líneas: {len(lines)}")
        print(f"   • Estaciones: {len(stations)}")
        print(f"   • Posts: {len(posts)}")
        print(f"   • Páginas: {len(pages)}")
        print(f"   • Proyectos: {len(projects)}")
        print(f"   • Eventos: {len(events)}")

    except Exception as e:
        print(f"❌ Error al crear datos: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚆 Iniciando creación de datos de prueba para el Blog Ferroviario...")
    create_sample_data()
    print("🎉 Proceso completado!")
