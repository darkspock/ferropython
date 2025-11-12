from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    author: str
    is_published: bool = True
    category_id: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    is_published: Optional[bool] = None
    category_id: Optional[int] = None


class Post(PostBase):
    id: int
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PageBase(BaseModel):
    title: str
    slug: str
    content: str
    is_published: bool = True


class PageCreate(PageBase):
    pass


class PageUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    is_published: Optional[bool] = None


class Page(PageBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Railway Line Models
class LineBase(BaseModel):
    line_number: str
    description: str
    status: str = "active"
    gauge_type: Optional[str] = None  # 'iberico', 'metrico', 'internacional'
    cities_served: List[str] = []
    category_id: Optional[int] = None


class LineCreate(LineBase):
    pass


class LineUpdate(BaseModel):
    line_number: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    gauge_type: Optional[str] = None
    cities_served: Optional[List[str]] = None
    category_id: Optional[int] = None


class Line(LineBase):
    id: int
    category_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Railway Station Models
class StationBase(BaseModel):
    station_code: str
    name: str
    address: str
    services: List[str] = []
    accessibility: List[str] = []
    station_type: Optional[str] = None  # 'principal', 'regional', 'local'
    province: Optional[str] = None
    city_id: Optional[int] = None


class StationCreate(StationBase):
    pass


class StationUpdate(BaseModel):
    station_code: Optional[str] = None
    name: Optional[str] = None
    address: Optional[str] = None
    services: Optional[List[str]] = None
    accessibility: Optional[List[str]] = None
    station_type: Optional[str] = None
    province: Optional[str] = None
    city_id: Optional[int] = None


class Station(StationBase):
    id: int
    city_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Railway Project Models
class ProjectBase(BaseModel):
    title: str
    description: str
    project_type: str
    budget: Optional[float] = None
    timeline: Optional[str] = None
    status: str = "planning"
    category_id: Optional[int] = None
    city_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    project_type: Optional[str] = None
    budget: Optional[float] = None
    timeline: Optional[str] = None
    status: Optional[str] = None
    category_id: Optional[int] = None
    city_id: Optional[int] = None


class Project(ProjectBase):
    id: int
    category_id: Optional[int] = None
    city_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Railway Event Models
class EventBase(BaseModel):
    title: str
    description: str
    event_date: datetime
    event_time: Optional[str] = None
    location: str
    event_type: str
    city_id: Optional[int] = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    event_date: Optional[datetime] = None
    event_time: Optional[str] = None
    location: Optional[str] = None
    event_type: Optional[str] = None
    city_id: Optional[int] = None


class Event(EventBase):
    id: int
    city_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# City Models
class CityBase(BaseModel):
    name: str
    slug: str
    region: str
    country: str = "Spain"


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


class City(CityBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Category Models
class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
