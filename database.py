import os
from typing import List, Optional
from datetime import datetime
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    desc,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from models import (
    Post,
    PostCreate,
    PostUpdate,
    Page,
    PageCreate,
    PageUpdate,
    Line,
    LineCreate,
    LineUpdate,
    Station,
    StationCreate,
    StationUpdate,
    Project,
    ProjectCreate,
    ProjectUpdate,
    Event,
    EventCreate,
    EventUpdate,
    City,
    CityCreate,
    CityUpdate,
    Category,
    CategoryCreate,
    CategoryUpdate,
)

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./blog.db")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# SQLAlchemy Post model
class PostModel(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author = Column(String(100), nullable=False)
    is_published = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("CategoryModel", back_populates="posts")


# SQLAlchemy Page model
class PageModel(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# SQLAlchemy Line model
class LineModel(Base):
    __tablename__ = "lines"

    id = Column(Integer, primary_key=True, index=True)
    line_number = Column(String(50), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="active")
    gauge_type = Column(String(50))  # 'iberico', 'metrico', 'internacional'
    cities_served = Column(Text)  # JSON string
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("CategoryModel", back_populates="lines")


# SQLAlchemy Station model
class StationModel(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    station_code = Column(String(20), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    address = Column(Text, nullable=False)
    services = Column(Text)  # JSON string
    accessibility = Column(Text)  # JSON string
    station_type = Column(String(50))  # 'principal', 'regional', 'local'
    province = Column(String(100))  # Provincia de la estación
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    city = relationship("CityModel", back_populates="stations")


# SQLAlchemy Project model
class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    project_type = Column(String(100), nullable=False)
    budget = Column(Integer)  # Store as cents/cents to avoid float issues
    timeline = Column(String(255))
    status = Column(String(50), default="planning")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("CategoryModel", back_populates="projects")
    city = relationship("CityModel", back_populates="projects")


# SQLAlchemy Event model
class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    event_date = Column(DateTime, nullable=False)
    event_time = Column(String(50))
    location = Column(String(255), nullable=False)
    event_type = Column(String(100), nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    city = relationship("CityModel", back_populates="events")


# SQLAlchemy City model
class CityModel(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    region = Column(String(255), nullable=False)
    country = Column(String(100), default="Spain")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    stations = relationship("StationModel", back_populates="city")
    projects = relationship("ProjectModel", back_populates="city")
    events = relationship("EventModel", back_populates="city")


# SQLAlchemy Category model
class CategoryModel(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    parent_id = Column(
        Integer, ForeignKey("categories.id"), nullable=True
    )  # Self-referencing for hierarchy
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    lines = relationship("LineModel", back_populates="category")
    projects = relationship("ProjectModel", back_populates="category")
    posts = relationship("PostModel", back_populates="category")
    parent = relationship("CategoryModel", remote_side=[id], back_populates="children")
    children = relationship("CategoryModel", back_populates="parent")


# Tables will be created by Alembic migrations
# Base.metadata.create_all(bind=engine)


class BlogDatabase:
    def __init__(self):
        pass

    def get_db(self):
        db = SessionLocal()
        try:
            return db
        finally:
            pass

    def create_post(self, post_data: PostCreate) -> Post:
        db = self.get_db()
        try:
            db_post = PostModel(
                title=post_data.title,
                content=post_data.content,
                author=post_data.author,
                is_published=post_data.is_published,
                category_id=post_data.category_id,
            )
            db.add(db_post)
            db.commit()
            db.refresh(db_post)

            # Convert SQLAlchemy model to Pydantic model
            return Post(
                id=int(db_post.id),
                title=str(db_post.title),
                content=str(db_post.content),
                author=str(db_post.author),
                is_published=bool(db_post.is_published),
                category_id=db_post.category_id,
                created_at=db_post.created_at,
                updated_at=db_post.updated_at,
            )
        finally:
            db.close()

    def get_post(self, post_id: int) -> Optional[Post]:
        db = self.get_db()
        try:
            db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
            if db_post:
                return Post(
                    id=int(db_post.id),
                    title=str(db_post.title),
                    content=str(db_post.content),
                    author=str(db_post.author),
                    is_published=bool(db_post.is_published),
                    category_id=db_post.category_id,
                    created_at=db_post.created_at,
                    updated_at=db_post.updated_at,
                )
            return None
        finally:
            db.close()

    def get_published_posts_paginated(self, page: int = 1, per_page: int = 5, category_id: Optional[int] = None):
        """Get paginated published posts with total count, optionally filtered by category"""
        db = self.get_db()
        try:
            # Build query
            query = db.query(PostModel).filter(PostModel.is_published == True)
            if category_id:
                query = query.filter(PostModel.category_id == category_id)
            
            # Count total published posts
            total_count = query.count()
            total_pages = (total_count + per_page - 1) // per_page

            # Get posts for current page - order by updated_at descending (most recent first)
            skip = (page - 1) * per_page
            posts = (
                query
                .order_by(desc(PostModel.updated_at), desc(PostModel.created_at))
                .offset(skip)
                .limit(per_page)
                .all()
            )

            post_list = [
                Post(
                    id=int(post.id),
                    title=str(post.title),
                    content=str(post.content),
                    author=str(post.author),
                    is_published=bool(post.is_published),
                    category_id=post.category_id,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
                for post in posts
            ]

            return post_list, total_pages
        finally:
            db.close()

    def get_posts(
        self,
        skip: int = 0,
        limit: int = 100,
        published_only: bool = True,
        category_id: Optional[int] = None,
    ) -> List[Post]:
        db = self.get_db()
        try:
            query = db.query(PostModel)
            if published_only:
                query = query.filter(PostModel.is_published == True)
            if category_id:
                query = query.filter(PostModel.category_id == category_id)
            posts = (
                query.order_by(desc(PostModel.updated_at), desc(PostModel.created_at))
                .offset(skip)
                .limit(limit)
                .all()
            )

            return [
                Post(
                    id=int(post.id),
                    title=str(post.title),
                    content=str(post.content),
                    author=str(post.author),
                    is_published=bool(post.is_published),
                    category_id=post.category_id,
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
                for post in posts
            ]
        finally:
            db.close()

    def update_post(self, post_id: int, post_data: PostUpdate) -> Optional[Post]:
        db = self.get_db()
        try:
            db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
            if db_post:
                update_data = post_data.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_post, field, value)
                # Update timestamp manually
                db_post.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_post)

                return Post(
                    id=int(db_post.id),
                    title=str(db_post.title),
                    content=str(db_post.content),
                    author=str(db_post.author),
                    is_published=bool(db_post.is_published),
                    category_id=db_post.category_id,
                    created_at=db_post.created_at,
                    updated_at=db_post.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_post(self, post_id: int) -> bool:
        db = self.get_db()
        try:
            db_post = db.query(PostModel).filter(PostModel.id == post_id).first()
            if db_post:
                db.delete(db_post)
                db.commit()
                return True
            return False
        finally:
            db.close()

    def search_posts(self, query: str, skip: int = 0, limit: int = 100) -> List[Post]:
        db = self.get_db()
        try:
            posts = (
                db.query(PostModel)
                .filter(
                    PostModel.is_published == True,
                    PostModel.title.contains(query) | PostModel.content.contains(query),
                )
                .order_by(desc(PostModel.created_at))
                .offset(skip)
                .limit(limit)
                .all()
            )

            return [
                Post(
                    id=int(post.id),
                    title=str(post.title),
                    content=str(post.content),
                    author=str(post.author),
                    is_published=bool(post.is_published),
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
                for post in posts
            ]
        finally:
            db.close()

    # Page methods
    def create_page(self, page_data: PageCreate) -> Page:
        db = self.get_db()
        try:
            db_page = PageModel(
                title=page_data.title,
                slug=page_data.slug,
                content=page_data.content,
                is_published=page_data.is_published,
            )
            db.add(db_page)
            db.commit()
            db.refresh(db_page)

            return Page(
                id=int(db_page.id),
                title=str(db_page.title),
                slug=str(db_page.slug),
                content=str(db_page.content),
                is_published=bool(db_page.is_published),
                created_at=db_page.created_at,
                updated_at=db_page.updated_at,
            )
        finally:
            db.close()

    def get_page(self, page_id: int) -> Optional[Page]:
        db = self.get_db()
        try:
            db_page = db.query(PageModel).filter(PageModel.id == page_id).first()
            if db_page:
                return Page(
                    id=int(db_page.id),
                    title=str(db_page.title),
                    slug=str(db_page.slug),
                    content=str(db_page.content),
                    is_published=bool(db_page.is_published),
                    created_at=db_page.created_at,
                    updated_at=db_page.updated_at,
                )
            return None
        finally:
            db.close()

    def get_page_by_slug(self, slug: str) -> Optional[Page]:
        db = self.get_db()
        try:
            db_page = db.query(PageModel).filter(PageModel.slug == slug).first()
            if db_page:
                return Page(
                    id=int(db_page.id),
                    title=str(db_page.title),
                    slug=str(db_page.slug),
                    content=str(db_page.content),
                    is_published=bool(db_page.is_published),
                    created_at=db_page.created_at,
                    updated_at=db_page.updated_at,
                )
            return None
        finally:
            db.close()

    def get_pages(
        self,
        skip: int = 0,
        limit: int = 100,
        published_only: bool = True,
    ) -> List[Page]:
        db = self.get_db()
        try:
            query = db.query(PageModel)
            if published_only:
                query = query.filter(PageModel.is_published == True)
            pages = (
                query.order_by(desc(PageModel.created_at))
                .offset(skip)
                .limit(limit)
                .all()
            )

            return [
                Page(
                    id=int(page.id),
                    title=str(page.title),
                    slug=str(page.slug),
                    content=str(page.content),
                    is_published=bool(page.is_published),
                    created_at=page.created_at,
                    updated_at=page.updated_at,
                )
                for page in pages
            ]
        finally:
            db.close()

    def update_page(self, page_id: int, page_data: PageUpdate) -> Optional[Page]:
        db = self.get_db()
        try:
            db_page = db.query(PageModel).filter(PageModel.id == page_id).first()
            if db_page:
                update_data = page_data.dict(exclude_unset=True)
                for field, value in update_data.items():
                    setattr(db_page, field, value)
                # Update timestamp manually
                db_page.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_page)

                return Page(
                    id=int(db_page.id),
                    title=str(db_page.title),
                    slug=str(db_page.slug),
                    content=str(db_page.content),
                    is_published=bool(db_page.is_published),
                    created_at=db_page.created_at,
                    updated_at=db_page.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_page(self, page_id: int) -> bool:
        db = self.get_db()
        try:
            db_page = db.query(PageModel).filter(PageModel.id == page_id).first()
            if db_page:
                db.delete(db_page)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Railway methods - Lines
    def get_lines(self, skip: int = 0, limit: int = 100, 
                  gauge_type: Optional[str] = None, 
                  status: Optional[str] = None) -> List[Line]:
        db = self.get_db()
        try:
            query = db.query(LineModel)
            if gauge_type:
                query = query.filter(LineModel.gauge_type == gauge_type)
            if status:
                query = query.filter(LineModel.status == status)
            lines = query.offset(skip).limit(limit).all()
            return [
                Line(
                    id=int(line.id),
                    line_number=str(line.line_number),
                    description=str(line.description),
                    status=str(line.status),
                    gauge_type=str(line.gauge_type) if line.gauge_type else None,
                    cities_served=line.cities_served.split(",")
                    if line.cities_served
                    else [],
                    category_id=line.category_id,
                    created_at=line.created_at,
                    updated_at=line.updated_at,
                )
                for line in lines
            ]
        finally:
            db.close()

    def get_line(self, line_id: int) -> Optional[Line]:
        db = self.get_db()
        try:
            line = db.query(LineModel).filter(LineModel.id == line_id).first()
            if line:
                return Line(
                    id=int(line.id),
                    line_number=str(line.line_number),
                    description=str(line.description),
                    status=str(line.status),
                    gauge_type=str(line.gauge_type) if line.gauge_type else None,
                    cities_served=line.cities_served.split(",")
                    if line.cities_served
                    else [],
                    category_id=line.category_id,
                    created_at=line.created_at,
                    updated_at=line.updated_at,
                )
            return None
        finally:
            db.close()

    def create_line(self, line_data: LineCreate) -> Line:
        db = self.get_db()
        try:
            db_line = LineModel(
                line_number=line_data.line_number,
                description=line_data.description,
                status=line_data.status,
                gauge_type=line_data.gauge_type,
                cities_served=",".join(line_data.cities_served)
                if line_data.cities_served
                else "",
                category_id=line_data.category_id,
            )
            db.add(db_line)
            db.commit()
            db.refresh(db_line)

            return Line(
                id=int(db_line.id),
                line_number=str(db_line.line_number),
                description=str(db_line.description),
                status=str(db_line.status),
                gauge_type=str(db_line.gauge_type) if db_line.gauge_type else None,
                cities_served=db_line.cities_served.split(",")
                if db_line.cities_served
                else [],
                category_id=db_line.category_id,
                created_at=db_line.created_at,
                updated_at=db_line.updated_at,
            )
        finally:
            db.close()

    def update_line(self, line_id: int, line_data: LineUpdate) -> Optional[Line]:
        db = self.get_db()
        try:
            db_line = db.query(LineModel).filter(LineModel.id == line_id).first()
            if db_line:
                if line_data.line_number is not None:
                    db_line.line_number = line_data.line_number
                # Allow empty strings for description
                if line_data.description is not None:
                    db_line.description = line_data.description or ""
                if line_data.status is not None:
                    db_line.status = line_data.status
                if line_data.gauge_type is not None:
                    db_line.gauge_type = line_data.gauge_type
                if line_data.cities_served is not None:
                    db_line.cities_served = (
                        ",".join(line_data.cities_served)
                        if line_data.cities_served
                        else ""
                    )
                if line_data.category_id is not None:
                    db_line.category_id = line_data.category_id

                db_line.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_line)

                return Line(
                    id=int(db_line.id),
                    line_number=str(db_line.line_number),
                    description=str(db_line.description),
                    status=str(db_line.status),
                    gauge_type=str(db_line.gauge_type) if db_line.gauge_type else None,
                    cities_served=db_line.cities_served.split(",")
                    if db_line.cities_served
                    else [],
                    category_id=db_line.category_id,
                    created_at=db_line.created_at,
                    updated_at=db_line.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_line(self, line_id: int) -> bool:
        db = self.get_db()
        try:
            db_line = db.query(LineModel).filter(LineModel.id == line_id).first()
            if db_line:
                db.delete(db_line)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Railway methods - Stations
    def get_stations(self, skip: int = 0, limit: int = 100,
                     station_type: Optional[str] = None,
                     city_id: Optional[int] = None,
                     province: Optional[str] = None) -> List[Station]:
        db = self.get_db()
        try:
            query = db.query(StationModel)
            if station_type:
                query = query.filter(StationModel.station_type == station_type)
            if city_id:
                query = query.filter(StationModel.city_id == city_id)
            if province:
                query = query.filter(StationModel.province.ilike(f"%{province}%"))
            stations = query.offset(skip).limit(limit).all()
            return [
                Station(
                    id=int(station.id),
                    station_code=str(station.station_code),
                    name=str(station.name),
                    address=str(station.address),
                    services=station.services.split(",") if station.services else [],
                    accessibility=station.accessibility.split(",")
                    if station.accessibility
                    else [],
                    station_type=str(station.station_type) if station.station_type else None,
                    province=str(station.province) if station.province else None,
                    city_id=station.city_id,
                    created_at=station.created_at,
                    updated_at=station.updated_at,
                )
                for station in stations
            ]
        finally:
            db.close()

    def get_station(self, station_id: int) -> Optional[Station]:
        db = self.get_db()
        try:
            station = (
                db.query(StationModel).filter(StationModel.id == station_id).first()
            )
            if station:
                return Station(
                    id=int(station.id),
                    station_code=str(station.station_code),
                    name=str(station.name),
                    address=str(station.address),
                    services=station.services.split(",") if station.services else [],
                    accessibility=station.accessibility.split(",")
                    if station.accessibility
                    else [],
                    station_type=str(station.station_type) if station.station_type else None,
                    province=str(station.province) if station.province else None,
                    city_id=station.city_id,
                    created_at=station.created_at,
                    updated_at=station.updated_at,
                )
            return None
        finally:
            db.close()

    # Railway methods - Projects
    def get_projects(self, skip: int = 0, limit: int = 100, 
                     status: Optional[str] = None) -> List[Project]:
        db = self.get_db()
        try:
            query = db.query(ProjectModel)
            if status:
                query = query.filter(ProjectModel.status == status)
            projects = query.offset(skip).limit(limit).all()
            return [
                Project(
                    id=int(project.id),
                    title=str(project.title),
                    description=str(project.description),
                    project_type=str(project.project_type),
                    budget=project.budget,
                    timeline=str(project.timeline),
                    status=str(project.status),
                    category_id=project.category_id,
                    city_id=project.city_id,
                    created_at=project.created_at,
                    updated_at=project.updated_at,
                )
                for project in projects
            ]
        finally:
            db.close()

    def get_project(self, project_id: int) -> Optional[Project]:
        db = self.get_db()
        try:
            project = (
                db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
            )
            if project:
                return Project(
                    id=int(project.id),
                    title=str(project.title),
                    description=str(project.description),
                    project_type=str(project.project_type),
                    budget=project.budget,
                    timeline=str(project.timeline),
                    status=str(project.status),
                    category_id=project.category_id,
                    city_id=project.city_id,
                    created_at=project.created_at,
                    updated_at=project.updated_at,
                )
            return None
        finally:
            db.close()

    def create_project(self, project_data: ProjectCreate) -> Project:
        db = self.get_db()
        try:
            db_project = ProjectModel(
                title=project_data.title,
                description=project_data.description,
                project_type=project_data.project_type,
                budget=project_data.budget,
                timeline=project_data.timeline,
                status=project_data.status,
                category_id=project_data.category_id,
                city_id=project_data.city_id,
            )
            db.add(db_project)
            db.commit()
            db.refresh(db_project)

            return Project(
                id=int(db_project.id),
                title=str(db_project.title),
                description=str(db_project.description),
                project_type=str(db_project.project_type),
                budget=db_project.budget,
                timeline=str(db_project.timeline),
                status=str(db_project.status),
                category_id=db_project.category_id,
                city_id=db_project.city_id,
                created_at=db_project.created_at,
                updated_at=db_project.updated_at,
            )
        finally:
            db.close()

    def update_project(
        self, project_id: int, project_data: ProjectUpdate
    ) -> Optional[Project]:
        db = self.get_db()
        try:
            db_project = (
                db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
            )
            if db_project:
                if project_data.title is not None:
                    db_project.title = project_data.title
                if project_data.description is not None:
                    db_project.description = project_data.description
                if project_data.project_type is not None:
                    db_project.project_type = project_data.project_type
                if project_data.budget is not None:
                    db_project.budget = project_data.budget
                if project_data.timeline is not None:
                    db_project.timeline = project_data.timeline
                if project_data.status is not None:
                    db_project.status = project_data.status
                if project_data.category_id is not None:
                    db_project.category_id = project_data.category_id
                if project_data.city_id is not None:
                    db_project.city_id = project_data.city_id

                db_project.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_project)

                return Project(
                    id=int(db_project.id),
                    title=str(db_project.title),
                    description=str(db_project.description),
                    project_type=str(db_project.project_type),
                    budget=db_project.budget,
                    timeline=str(db_project.timeline),
                    status=str(db_project.status),
                    category_id=db_project.category_id,
                    city_id=db_project.city_id,
                    created_at=db_project.created_at,
                    updated_at=db_project.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_project(self, project_id: int) -> bool:
        db = self.get_db()
        try:
            db_project = (
                db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
            )
            if db_project:
                db.delete(db_project)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Railway methods - Events
    def get_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        db = self.get_db()
        try:
            events = db.query(EventModel).offset(skip).limit(limit).all()
            return [
                Event(
                    id=int(event.id),
                    title=str(event.title),
                    description=str(event.description),
                    event_date=event.event_date,
                    event_time=str(event.event_time),
                    location=str(event.location),
                    event_type=str(event.event_type),
                    city_id=event.city_id,
                    created_at=event.created_at,
                    updated_at=event.updated_at,
                )
                for event in events
            ]
        finally:
            db.close()

    def get_event(self, event_id: int) -> Optional[Event]:
        db = self.get_db()
        try:
            event = db.query(EventModel).filter(EventModel.id == event_id).first()
            if event:
                return Event(
                    id=int(event.id),
                    title=str(event.title),
                    description=str(event.description),
                    event_date=event.event_date,
                    event_time=str(event.event_time),
                    location=str(event.location),
                    event_type=str(event.event_type),
                    city_id=event.city_id,
                    created_at=event.created_at,
                    updated_at=event.updated_at,
                )
            return None
        finally:
            db.close()

    # Railway methods - Cities
    def get_cities(self, skip: int = 0, limit: int = 100, 
                   name: Optional[str] = None) -> List[City]:
        db = self.get_db()
        try:
            query = db.query(CityModel)
            if name:
                query = query.filter(CityModel.name.ilike(f"%{name}%"))
            cities = query.offset(skip).limit(limit).all()
            return [
                City(
                    id=int(city.id),
                    name=str(city.name),
                    slug=str(city.slug),
                    region=str(city.region),
                    country=str(city.country),
                    created_at=city.created_at,
                    updated_at=city.updated_at,
                )
                for city in cities
            ]
        finally:
            db.close()

    def get_city(self, city_id: int) -> Optional[City]:
        db = self.get_db()
        try:
            city = db.query(CityModel).filter(CityModel.id == city_id).first()
            if city:
                return City(
                    id=int(city.id),
                    name=str(city.name),
                    slug=str(city.slug),
                    region=str(city.region),
                    country=str(city.country),
                    created_at=city.created_at,
                    updated_at=city.updated_at,
                )
            return None
        finally:
            db.close()

    def get_city_by_slug(self, slug: str) -> Optional[City]:
        db = self.get_db()
        try:
            city = db.query(CityModel).filter(CityModel.slug == slug).first()
            if city:
                return City(
                    id=int(city.id),
                    name=str(city.name),
                    slug=str(city.slug),
                    region=str(city.region),
                    country=str(city.country),
                    created_at=city.created_at,
                    updated_at=city.updated_at,
                )
            return None
        finally:
            db.close()

    # Railway methods - Categories
    def get_categories(self, skip: int = 0, limit: int = 100) -> List[Category]:
        db = self.get_db()
        try:
            categories = db.query(CategoryModel).offset(skip).limit(limit).all()
            return [
                Category(
                    id=int(category.id),
                    name=str(category.name),
                    slug=str(category.slug),
                    description=str(category.description)
                    if category.description
                    else None,
                    parent_id=category.parent_id,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
                for category in categories
            ]
        finally:
            db.close()

    def get_category(self, category_id: int) -> Optional[Category]:
        db = self.get_db()
        try:
            category = (
                db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            )
            if category:
                return Category(
                    id=int(category.id),
                    name=str(category.name),
                    slug=str(category.slug),
                    description=str(category.description)
                    if category.description
                    else None,
                    parent_id=category.parent_id,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
            return None
        finally:
            db.close()

    def get_category_by_slug(self, slug: str) -> Optional[Category]:
        db = self.get_db()
        try:
            category = (
                db.query(CategoryModel).filter(CategoryModel.slug == slug).first()
            )
            if category:
                return Category(
                    id=int(category.id),
                    name=str(category.name),
                    slug=str(category.slug),
                    description=str(category.description)
                    if category.description
                    else None,
                    parent_id=category.parent_id,
                    created_at=category.created_at,
                    updated_at=category.updated_at,
                )
            return None
        finally:
            db.close()

    # Station CRUD methods
    def create_station(self, station_data: StationCreate) -> Station:
        db = self.get_db()
        try:
            db_station = StationModel(
                station_code=station_data.station_code,
                name=station_data.name,
                address=station_data.address,
                services=",".join(station_data.services)
                if station_data.services
                else "",
                accessibility=",".join(station_data.accessibility)
                if station_data.accessibility
                else "",
                station_type=station_data.station_type,
                province=station_data.province,
                city_id=station_data.city_id,
            )
            db.add(db_station)
            db.commit()
            db.refresh(db_station)

            return Station(
                id=int(db_station.id),
                station_code=str(db_station.station_code),
                name=str(db_station.name),
                address=str(db_station.address),
                services=db_station.services.split(",") if db_station.services else [],
                accessibility=db_station.accessibility.split(",")
                if db_station.accessibility
                else [],
                station_type=str(db_station.station_type) if db_station.station_type else None,
                province=str(db_station.province) if db_station.province else None,
                city_id=db_station.city_id,
                created_at=db_station.created_at,
                updated_at=db_station.updated_at,
            )
        finally:
            db.close()

    def update_station(
        self, station_id: int, station_data: StationUpdate
    ) -> Optional[Station]:
        db = self.get_db()
        try:
            db_station = (
                db.query(StationModel).filter(StationModel.id == station_id).first()
            )
            if db_station:
                if station_data.station_code is not None:
                    db_station.station_code = station_data.station_code
                if station_data.name is not None:
                    db_station.name = station_data.name
                if station_data.address is not None:
                    db_station.address = station_data.address
                if station_data.services is not None:
                    db_station.services = ",".join(station_data.services)
                if station_data.accessibility is not None:
                    db_station.accessibility = ",".join(station_data.accessibility)
                if station_data.station_type is not None:
                    db_station.station_type = station_data.station_type
                if station_data.province is not None:
                    db_station.province = station_data.province
                if station_data.city_id is not None:
                    db_station.city_id = station_data.city_id

                db_station.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_station)

                return Station(
                    id=int(db_station.id),
                    station_code=str(db_station.station_code),
                    name=str(db_station.name),
                    address=str(db_station.address),
                    services=db_station.services.split(",")
                    if db_station.services
                    else [],
                    accessibility=db_station.accessibility.split(",")
                    if db_station.accessibility
                    else [],
                    station_type=str(db_station.station_type) if db_station.station_type else None,
                    province=str(db_station.province) if db_station.province else None,
                    city_id=db_station.city_id,
                    created_at=db_station.created_at,
                    updated_at=db_station.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_station(self, station_id: int) -> bool:
        db = self.get_db()
        try:
            db_station = (
                db.query(StationModel).filter(StationModel.id == station_id).first()
            )
            if db_station:
                db.delete(db_station)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Event CRUD methods
    def create_event(self, event_data: EventCreate) -> Event:
        db = self.get_db()
        try:
            db_event = EventModel(
                title=event_data.title,
                description=event_data.description,
                event_date=event_data.event_date,
                event_time=event_data.event_time,
                location=event_data.location,
                event_type=event_data.event_type,
                city_id=event_data.city_id,
            )
            db.add(db_event)
            db.commit()
            db.refresh(db_event)

            return Event(
                id=int(db_event.id),
                title=str(db_event.title),
                description=str(db_event.description),
                event_date=db_event.event_date,
                event_time=str(db_event.event_time),
                location=str(db_event.location),
                event_type=str(db_event.event_type),
                city_id=db_event.city_id,
                created_at=db_event.created_at,
                updated_at=db_event.updated_at,
            )
        finally:
            db.close()

    def update_event(self, event_id: int, event_data: EventUpdate) -> Optional[Event]:
        db = self.get_db()
        try:
            db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
            if db_event:
                if event_data.title is not None:
                    db_event.title = event_data.title
                if event_data.description is not None:
                    db_event.description = event_data.description
                if event_data.event_date is not None:
                    db_event.event_date = event_data.event_date
                if event_data.event_time is not None:
                    db_event.event_time = event_data.event_time
                if event_data.location is not None:
                    db_event.location = event_data.location
                if event_data.event_type is not None:
                    db_event.event_type = event_data.event_type
                if event_data.city_id is not None:
                    db_event.city_id = event_data.city_id

                db_event.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_event)

                return Event(
                    id=int(db_event.id),
                    title=str(db_event.title),
                    description=str(db_event.description),
                    event_date=db_event.event_date,
                    event_time=str(db_event.event_time),
                    location=str(db_event.location),
                    event_type=str(db_event.event_type),
                    city_id=db_event.city_id,
                    created_at=db_event.created_at,
                    updated_at=db_event.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_event(self, event_id: int) -> bool:
        db = self.get_db()
        try:
            db_event = db.query(EventModel).filter(EventModel.id == event_id).first()
            if db_event:
                db.delete(db_event)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # City CRUD methods
    def create_city(self, city_data: CityCreate) -> City:
        db = self.get_db()
        try:
            db_city = CityModel(
                name=city_data.name,
                slug=city_data.slug,
                region=city_data.region,
                country=city_data.country,
            )
            db.add(db_city)
            db.commit()
            db.refresh(db_city)

            return City(
                id=int(db_city.id),
                name=str(db_city.name),
                slug=str(db_city.slug),
                region=str(db_city.region),
                country=str(db_city.country),
                created_at=db_city.created_at,
                updated_at=db_city.updated_at,
            )
        finally:
            db.close()

    def update_city(self, city_id: int, city_data: CityUpdate) -> Optional[City]:
        db = self.get_db()
        try:
            db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
            if db_city:
                if city_data.name is not None:
                    db_city.name = city_data.name
                if city_data.slug is not None:
                    db_city.slug = city_data.slug
                if city_data.region is not None:
                    db_city.region = city_data.region
                if city_data.country is not None:
                    db_city.country = city_data.country

                db_city.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_city)

                return City(
                    id=int(db_city.id),
                    name=str(db_city.name),
                    slug=str(db_city.slug),
                    region=str(db_city.region),
                    country=str(db_city.country),
                    created_at=db_city.created_at,
                    updated_at=db_city.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_city(self, city_id: int) -> bool:
        db = self.get_db()
        try:
            db_city = db.query(CityModel).filter(CityModel.id == city_id).first()
            if db_city:
                db.delete(db_city)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Category CRUD methods
    def create_category(self, category_data: CategoryCreate) -> Category:
        db = self.get_db()
        try:
            db_category = CategoryModel(
                name=category_data.name,
                slug=category_data.slug,
                description=category_data.description,
                parent_id=category_data.parent_id,
            )
            db.add(db_category)
            db.commit()
            db.refresh(db_category)

            return Category(
                id=int(db_category.id),
                name=str(db_category.name),
                slug=str(db_category.slug),
                description=str(db_category.description)
                if db_category.description
                else None,
                parent_id=db_category.parent_id,
                created_at=db_category.created_at,
                updated_at=db_category.updated_at,
            )
        finally:
            db.close()

    def update_category(
        self, category_id: int, category_data: CategoryUpdate
    ) -> Optional[Category]:
        db = self.get_db()
        try:
            db_category = (
                db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            )
            if db_category:
                if category_data.name is not None:
                    db_category.name = category_data.name
                if category_data.slug is not None:
                    db_category.slug = category_data.slug
                if category_data.description is not None:
                    db_category.description = category_data.description
                if category_data.parent_id is not None:
                    db_category.parent_id = category_data.parent_id

                db_category.updated_at = datetime.utcnow()
                db.commit()
                db.refresh(db_category)

                return Category(
                    id=int(db_category.id),
                    name=str(db_category.name),
                    slug=str(db_category.slug),
                    description=str(db_category.description)
                    if db_category.description
                    else None,
                    parent_id=db_category.parent_id,
                    created_at=db_category.created_at,
                    updated_at=db_category.updated_at,
                )
            return None
        finally:
            db.close()

    def delete_category(self, category_id: int) -> bool:
        db = self.get_db()
        try:
            db_category = (
                db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
            )
            if db_category:
                db.delete(db_category)
                db.commit()
                return True
            return False
        finally:
            db.close()

    # Search method for posts
    def search_posts_paginated(self, query: str, page: int = 1, per_page: int = 5):
        """Get paginated search results for posts"""
        db = self.get_db()
        try:
            # Count total matching posts
            total_count = (
                db.query(PostModel)
                .filter(
                    PostModel.is_published == True,
                    PostModel.title.contains(query) | PostModel.content.contains(query),
                )
                .count()
            )
            total_pages = (total_count + per_page - 1) // per_page

            # Get posts for current page
            skip = (page - 1) * per_page
            posts = (
                db.query(PostModel)
                .filter(
                    PostModel.is_published == True,
                    PostModel.title.contains(query) | PostModel.content.contains(query),
                )
                .order_by(desc(PostModel.created_at))
                .offset(skip)
                .limit(per_page)
                .all()
            )

            post_list = [
                Post(
                    id=int(post.id),
                    title=str(post.title),
                    content=str(post.content),
                    author=str(post.author),
                    is_published=bool(post.is_published),
                    created_at=post.created_at,
                    updated_at=post.updated_at,
                )
                for post in posts
            ]

            return post_list, total_pages
        finally:
            db.close()

    def get_recent_entries(self, limit: int = 5) -> List[dict]:
        """Get the most recent entries from all entities (posts, lines, stations, projects, cities)"""
        db = self.get_db()
        try:
            entries = []
            
            # Get recent posts
            posts = db.query(PostModel).filter(PostModel.is_published == True).order_by(desc(PostModel.updated_at)).limit(limit * 2).all()
            for post in posts:
                entries.append({
                    'type': 'post',
                    'title': post.title,
                    'url': f'/post/{post.id}',
                    'updated_at': post.updated_at or post.created_at,
                })
            
            # Get recent lines
            lines = db.query(LineModel).order_by(desc(LineModel.updated_at)).limit(limit * 2).all()
            for line in lines:
                entries.append({
                    'type': 'line',
                    'title': f'Línea {line.line_number}',
                    'url': f'/lines/{line.id}',
                    'updated_at': line.updated_at or line.created_at,
                })
            
            # Get recent stations
            stations = db.query(StationModel).order_by(desc(StationModel.updated_at)).limit(limit * 2).all()
            for station in stations:
                entries.append({
                    'type': 'station',
                    'title': station.name,
                    'url': f'/stations/{station.id}',
                    'updated_at': station.updated_at or station.created_at,
                })
            
            # Get recent projects
            projects = db.query(ProjectModel).order_by(desc(ProjectModel.updated_at)).limit(limit * 2).all()
            for project in projects:
                entries.append({
                    'type': 'project',
                    'title': project.title,
                    'url': f'/projects/{project.id}',
                    'updated_at': project.updated_at or project.created_at,
                })
            
            # Get recent cities
            cities = db.query(CityModel).order_by(desc(CityModel.updated_at)).limit(limit * 2).all()
            for city in cities:
                entries.append({
                    'type': 'city',
                    'title': city.name,
                    'url': f'/cities/{city.slug}',
                    'updated_at': city.updated_at or city.created_at,
                })
            
            # Sort all entries by updated_at descending and take the most recent ones
            entries.sort(key=lambda x: x['updated_at'], reverse=True)
            return entries[:limit]
        finally:
            db.close()


# Create database instance
db = BlogDatabase()
