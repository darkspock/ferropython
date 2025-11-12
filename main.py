from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List, Optional
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
from database import db
from auth import (
    AuthMiddleware,
    ADMIN_PASSWORD,
    SECRET_KEY,
    set_auth_cookie,
    clear_auth_cookie,
)


class Pagination:
    def __init__(self, page: int, total_pages: int, per_page: int = 5):
        self.page = page
        self.total_pages = total_pages
        self.per_page = per_page
        self.has_prev = page > 1
        self.has_next = page < total_pages
        self.prev_num = page - 1 if self.has_prev else None
        self.next_num = page + 1 if self.has_next else None

    def iter_pages(self):
        """Generate page numbers for pagination display."""
        left_edge = 2
        left_current = 2
        right_current = 3
        right_edge = 2

        if self.total_pages <= (left_edge + left_current + right_current + right_edge):
            # Not enough pages to break it up
            for num in range(1, self.total_pages + 1):
                yield num
        else:
            # Enough pages to break it up
            last = 0
            for num in range(1, self.total_pages + 1):
                if (
                    num <= left_edge
                    or (
                        num > self.page - left_current - 1
                        and num < self.page + right_current
                    )
                    or num > self.total_pages - right_edge
                ):
                    if last + 1 != num:
                        yield None  # Ellipsis
                    yield num
                    last = num


app = FastAPI(title="Blog API", description="A simple blog built with FastAPI")

# Add authentication middleware
app.add_middleware(AuthMiddleware)


def is_authenticated(request: Request) -> bool:
    """Check if user is authenticated."""
    auth_token = request.cookies.get("auth_token")
    return auth_token == SECRET_KEY


def get_template_context(request: Request) -> dict:
    """Get common template context for all pages"""
    return {
        "is_admin": is_authenticated(request),
        "recent_entries": db.get_recent_entries(limit=5),
    }


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

import re
from jinja2 import Environment


def strip_html(text):
    """Strip HTML tags from text and truncate to 150 characters."""
    if not text:
        return ""
    # Remove HTML tags
    clean_text = re.sub(r"<[^>]+>", "", text)
    # Truncate to 150 characters
    if len(clean_text) > 150:
        clean_text = clean_text[:150] + "..."
    return clean_text


# Add custom filters to Jinja2 environment
templates.env.filters["strip_html"] = strip_html


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Redirect to /posts/noticias by default
    return RedirectResponse(url="/posts/noticias", status_code=303)


def render_template(request: Request, template_name: str, context: dict = None):
    """Helper function to render template with common context"""
    if context is None:
        context = {}
    # Merge common context with provided context
    common_context = get_template_context(request)
    context.update(common_context)
    return templates.TemplateResponse(template_name, {"request": request, **context})


@app.get("/post/{post_id}", response_class=HTMLResponse)
async def get_post(request: Request, post_id: int):
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return render_template(request, "post.html", {"post": post})


@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request, error: str = ""):
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": error}
    )


@app.post("/login")
async def login(request: Request, email: str = Form(""), password: str = Form(...)):
    if password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/", status_code=303)
        return set_auth_cookie(response, SECRET_KEY)
    else:
        return templates.TemplateResponse(
            "login.html", {"request": request, "error": "Invalid password"}
        )


@app.post("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    return clear_auth_cookie(response)


@app.get("/admin", response_class=HTMLResponse)
async def admin_redirect(request: Request):
    return RedirectResponse(url="/admin/dashboard", status_code=302)


@app.get("/admin/posts", response_class=HTMLResponse)
async def admin_posts(request: Request):
    try:
        posts = db.get_posts(published_only=False, limit=1000)
    except:
        posts = []
    categories = db.get_categories()
    return templates.TemplateResponse(
        "admin_posts.html",
        {
            "request": request,
            "posts": posts,
            "categories": categories,
        },
    )


@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard_main(request: Request):
    try:
        # Get statistics with fallback values
        try:
            all_posts = db.get_posts(published_only=False) or []
            posts_count = len(all_posts)
            recent_posts = all_posts[:5]
        except:
            posts_count = 0
            recent_posts = []

        try:
            all_lines = db.get_lines() or []
            lines_count = len(all_lines)
        except:
            lines_count = 0

        try:
            all_stations = db.get_stations() or []
            stations_count = len(all_stations)
        except:
            stations_count = 0

        try:
            all_projects = db.get_projects() or []
            projects_count = len(all_projects)
        except:
            projects_count = 0

        try:
            all_events = db.get_events() or []
            recent_events = sorted(
                all_events,
                key=lambda x: x.event_date if x.event_date else "",
                reverse=True,
            )[:5]
        except:
            recent_events = []

        stats = {
            "posts_count": posts_count,
            "lines_count": lines_count,
            "stations_count": stations_count,
            "projects_count": projects_count,
        }

        return templates.TemplateResponse(
            "admin_dashboard.html",
            {
                "request": request,
                "stats": stats,
                "recent_posts": recent_posts,
                "recent_events": recent_events,
            },
        )
    except Exception as e:
        # Return a simple error page if something goes wrong
        return HTMLResponse(f"<h1>Error</h1><p>{str(e)}</p>")


@app.get("/new", response_class=HTMLResponse)
async def new_post_form(request: Request):
    # Get all categories, but filter to show only Noticias, Curiosidades, and Eventos for posts
    all_categories = db.get_categories()
    # Filter to only show the main post categories (Noticias, Curiosidades, Eventos)
    post_categories = [cat for cat in all_categories if cat.slug in ['noticias', 'curiosidades', 'eventos']]
    # If those don't exist, show all categories as fallback
    categories = post_categories if post_categories else all_categories
    return templates.TemplateResponse("new_post.html", {"request": request, "categories": categories})


@app.post("/posts")
async def create_post(
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    is_published: bool = Form(True),
    category_id: Optional[int] = Form(None),
):
    post_data = PostCreate(
        title=title, content=content, author=author, is_published=is_published, category_id=category_id
    )
    post = db.create_post(post_data)
    return RedirectResponse(url=f"/post/{post.id}", status_code=303)


@app.get("/edit/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int):
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Filter to only show the main post categories (Noticias, Curiosidades, Eventos)
    all_categories = db.get_categories()
    post_categories = [cat for cat in all_categories if cat.slug in ['noticias', 'curiosidades', 'eventos']]
    # If those don't exist, show all categories as fallback
    categories = post_categories if post_categories else all_categories
    return templates.TemplateResponse(
        "edit_post.html", {"request": request, "post": post, "categories": categories}
    )


# Posts by Category Route - MUST be before /posts/{post_id} routes
# This route handles /posts/{category_slug} where category_slug is a string (not numeric)
@app.get("/posts/{category_slug}", response_class=HTMLResponse)
async def list_posts_by_category(request: Request, category_slug: str, page: int = 1):
    # Validate that category_slug is not numeric (to avoid conflicts with /posts/{post_id})
    # If it's numeric, it should go to /post/{post_id} instead
    if category_slug.isdigit():
        raise HTTPException(status_code=404, detail="Use /post/{post_id} to view individual posts")
    
    # Get category by slug
    try:
        category = db.get_category_by_slug(category_slug)
    except Exception as e:
        # Log error and show all posts
        print(f"Error getting category by slug '{category_slug}': {e}")
        posts, total_pages = db.get_published_posts_paginated(page, per_page=10, category_id=None)
        pagination = Pagination(page, total_pages, per_page=10)
        return render_template(
            request,
            "index.html",
            {
                "posts": posts,
                "pagination": pagination,
                "category_id": None,
                "category": None,
                "error_message": f"Error al buscar la categoría '{category_slug}'. Mostrando todos los posts.",
            },
        )
    
    if not category:
        # If category doesn't exist, show all posts with a message
        posts, total_pages = db.get_published_posts_paginated(page, per_page=10, category_id=None)
        pagination = Pagination(page, total_pages, per_page=10)
        return render_template(
            request,
            "index.html",
            {
                "posts": posts,
                "pagination": pagination,
                "category_id": None,
                "category": None,
                "error_message": f"La categoría '{category_slug}' no existe. Mostrando todos los posts.",
            },
        )
    
    # Get posts filtered by category
    posts, total_pages = db.get_published_posts_paginated(page, per_page=10, category_id=category.id)
    pagination = Pagination(page, total_pages, per_page=10)
    
    # Use index.html template for posts listing
    return render_template(
        request,
        "index.html",
        {
            "posts": posts,
            "pagination": pagination,
            "category_id": category.id,
            "category": category,
        },
    )


@app.post("/posts/{post_id}")
async def update_post(
    post_id: int,
    title: str = Form(...),
    content: str = Form(...),
    author: str = Form(...),
    is_published: bool = Form(False),
    category_id: Optional[int] = Form(None),
):
    post_data = PostUpdate(
        title=title, content=content, author=author, is_published=is_published, category_id=category_id
    )
    post = db.update_post(post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse(url=f"/post/{post.id}", status_code=303)


@app.post("/posts/{post_id}/delete")
async def delete_post(post_id: int):
    success = db.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return RedirectResponse(url="/", status_code=303)


# API Endpoints
@app.get("/api/posts", response_model=List[Post])
async def api_get_all_posts():
    return db.get_posts(published_only=False)


@app.get("/api/posts/{post_id}", response_model=Post)
async def api_get_post(post_id: int):
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.post("/api/posts", response_model=Post)
async def api_create_post(post_data: PostCreate):
    return db.create_post(post_data)


@app.put("/api/posts/{post_id}", response_model=Post)
async def api_update_post(post_id: int, post_data: PostUpdate):
    post = db.update_post(post_id, post_data)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/search", response_class=HTMLResponse)
async def search_posts(request: Request, q: str = "", page: int = 1):
    if not q.strip():
        return RedirectResponse(url="/", status_code=303)

    posts, total_pages = db.search_posts_paginated(q, page, per_page=5)
    pagination = Pagination(page, total_pages, per_page=5)
    return render_template(
        request,
        "search.html",
        {
            "posts": posts,
            "query": q,
            "pagination": pagination,
        },
    )


@app.delete("/api/posts/{post_id}")
async def api_delete_post(post_id: int):
    success = db.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}


# Page routes
@app.get("/admin/pages", response_class=HTMLResponse)
async def admin_pages(request: Request):
    pages = db.get_pages(published_only=False)
    return templates.TemplateResponse(
        "admin_pages.html",
        {
            "request": request,
            "pages": pages,
        },
    )


@app.get("/admin/pages/new", response_class=HTMLResponse)
async def new_page_form(request: Request):
    return templates.TemplateResponse("new_page.html", {"request": request})


@app.post("/admin/pages")
async def create_page(
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(...),
    is_published: bool = Form(False),
):
    page_data = PageCreate(
        title=title, slug=slug, content=content, is_published=is_published
    )
    db.create_page(page_data)
    return RedirectResponse(url="/admin/pages", status_code=303)


@app.get("/pages/{slug}", response_class=HTMLResponse)
async def get_page(request: Request, slug: str):
    page = db.get_page_by_slug(slug)
    if not page or not page.is_published:
        raise HTTPException(status_code=404, detail="Page not found")
    return render_template(request, "page.html", {"page": page})


@app.get("/admin/pages/{page_id}/edit", response_class=HTMLResponse)
async def edit_page_form(request: Request, page_id: int):
    page = db.get_page(page_id)
    if not page:
        raise HTTPException(status_code=404, detail="Page not found")
    return templates.TemplateResponse(
        "edit_page.html", {"request": request, "page": page}
    )


@app.post("/admin/pages/{page_id}")
async def update_page(
    page_id: int,
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(...),
    is_published: bool = Form(False),
):
    page_data = PageUpdate(
        title=title, slug=slug, content=content, is_published=is_published
    )
    success = db.update_page(page_id, page_data)
    if not success:
        raise HTTPException(status_code=404, detail="Page not found")
    return RedirectResponse(url="/admin/pages", status_code=303)


@app.post("/admin/pages/{page_id}/delete")
async def delete_page(page_id: int):
    success = db.delete_page(page_id)
    if not success:
        raise HTTPException(status_code=404, detail="Page not found")
    return RedirectResponse(url="/admin/pages", status_code=303)


# Railway Routes - Lines
@app.get("/lines", response_class=HTMLResponse)
async def list_lines(
    request: Request,
    type: Optional[str] = None,
    status: Optional[str] = None
):
    # Map 'type' parameter to 'gauge_type' for database query
    gauge_type = None
    if type:
        # Map URL parameter values to database values
        type_map = {
            "iberico": "iberico",
            "metrico": "metrico",
            "internacional": "internacional"
        }
        gauge_type = type_map.get(type)
    
    # Map 'status' parameter
    line_status = None
    if status:
        status_map = {
            "cerrada": "cerrada",
            "active": "active"
        }
        line_status = status_map.get(status, status)
    
    lines = db.get_lines(gauge_type=gauge_type, status=line_status)
    return render_template(
        request,
        "lines.html",
        {
            "lines": lines,
            "filter_type": type,
            "filter_status": status,
        },
    )


@app.get("/lines/new", response_class=HTMLResponse)
async def lines_new_redirect(request: Request):
    """Redirect /lines/new to /admin/lines/new"""
    return RedirectResponse(url="/admin/lines/new", status_code=303)


@app.get("/lines/{line_id}", response_class=HTMLResponse)
async def get_line(request: Request, line_id: int):
    line = db.get_line(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    return render_template(request, "line.html", {"line": line})


# Railway Routes - Stations
@app.get("/stations", response_class=HTMLResponse)
async def list_stations(
    request: Request,
    type: Optional[str] = None,
    city_id: Optional[int] = None,
    province: Optional[str] = None
):
    # Map 'type' parameter to 'station_type'
    station_type = None
    if type:
        type_map = {
            "principal": "principal",
            "regional": "regional",
            "local": "local"
        }
        station_type = type_map.get(type)
    
    stations = db.get_stations(
        station_type=station_type,
        city_id=city_id,
        province=province
    )
    
    # Add city names to each station
    stations_with_names = []
    for station in stations:
        station_dict = station.model_dump()
        city_name = None
        if station.city_id:
            city = db.get_city(station.city_id)
            if city:
                city_name = city.name
        station_dict['city_name'] = city_name
        stations_with_names.append(station_dict)
    
    return render_template(
        request,
        "stations.html",
        {
            "stations": stations_with_names,
            "filter_type": type,
            "filter_city_id": city_id,
            "filter_province": province,
        },
    )


@app.get("/stations/new", response_class=HTMLResponse)
async def stations_new_redirect(request: Request):
    """Redirect /stations/new to /admin/stations/new"""
    return RedirectResponse(url="/admin/stations/new", status_code=303)


@app.get("/stations/{station_id}", response_class=HTMLResponse)
async def get_station(request: Request, station_id: int):
    station = db.get_station(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    
    # Get city name if it exists
    city_name = None
    if station.city_id:
        city = db.get_city(station.city_id)
        if city:
            city_name = city.name
    
    # Add name to station object for template
    station_dict = station.model_dump()
    station_dict['city_name'] = city_name
    
    return render_template(request, "station.html", {"station": station_dict})


# Railway Routes - Projects
@app.get("/projects", response_class=HTMLResponse)
async def list_projects(
    request: Request,
    status: Optional[str] = None
):
    # Map status parameter values
    project_status = None
    if status:
        # Accept both old and new status values for backward compatibility
        status_map = {
            "cancelado": "suspended",
            "en-marcha": "construction",
            "en-estudio": "planning",
            "actual": "construction",
            "planning": "planning",
            "construction": "construction",
            "completed": "completed",
            "suspended": "suspended"
        }
        project_status = status_map.get(status, status)
    
    projects = db.get_projects(status=project_status)
    
    # Add category and city names to each project
    projects_with_names = []
    for project in projects:
        project_dict = project.model_dump()
        category_name = None
        city_name = None
        if project.category_id:
            category = db.get_category(project.category_id)
            if category:
                category_name = category.name
        if project.city_id:
            city = db.get_city(project.city_id)
            if city:
                city_name = city.name
        project_dict['category_name'] = category_name
        project_dict['city_name'] = city_name
        projects_with_names.append(project_dict)
    
    return render_template(
        request,
        "projects.html",
        {
            "projects": projects_with_names,
            "filter_status": status,
        },
    )


@app.get("/projects/new", response_class=HTMLResponse)
async def projects_new_redirect(request: Request):
    """Redirect /projects/new to /admin/projects/new"""
    return RedirectResponse(url="/admin/projects/new", status_code=303)


@app.get("/projects/{project_id}", response_class=HTMLResponse)
async def get_project(request: Request, project_id: int):
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get category and city names if they exist
    category_name = None
    city_name = None
    if project.category_id:
        category = db.get_category(project.category_id)
        if category:
            category_name = category.name
    if project.city_id:
        city = db.get_city(project.city_id)
        if city:
            city_name = city.name
    
    # Add names to project object for template
    project_dict = project.model_dump()
    project_dict['category_name'] = category_name
    project_dict['city_name'] = city_name
    
    return render_template(request, "project.html", {"project": project_dict})


# Railway Routes - Cities
@app.get("/cities", response_class=HTMLResponse)
async def list_cities(
    request: Request,
    name: Optional[str] = None
):
    cities = db.get_cities(name=name)
    
    # If a city name is provided, get related content
    related_lines = []
    related_stations = []
    related_projects = []
    
    if name:
        # Get city by name to get its ID
        city_list = db.get_cities(name=name, skip=0, limit=1)
        if city_list:
            city = city_list[0]
            # Get related content
            all_lines = db.get_lines()
            related_lines = [line for line in all_lines if city.name in (line.cities_served or [])]
            
            all_stations = db.get_stations(city_id=city.id)
            related_stations = all_stations
            
            all_projects = db.get_projects()
            related_projects = [p for p in all_projects if p.city_id == city.id]
    
    return render_template(
        request,
        "cities.html",
        {
            "cities": cities,
            "filter_name": name,
            "related_lines": related_lines if name else [],
            "related_stations": related_stations if name else [],
            "related_projects": related_projects if name else [],
        },
    )


@app.get("/cities/{slug}", response_class=HTMLResponse)
async def get_city(request: Request, slug: str):
    # Try to get by slug first, then by ID if slug is numeric
    city = None
    if slug.isdigit():
        city = db.get_city(int(slug))
    else:
        city = db.get_city_by_slug(slug)
    
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return render_template(request, "city.html", {"city": city})


# Railway Routes - Categories
@app.get("/categories", response_class=HTMLResponse)
async def list_categories(request: Request):
    categories = db.get_categories()
    return render_template(request, "categories.html", {"categories": categories})


@app.get("/categories/{category_id}", response_class=HTMLResponse)
async def get_category(request: Request, category_id: int):
    category = db.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return render_template(request, "category.html", {"category": category})


# Form Routes - Lines
@app.get("/admin/lines/new", response_class=HTMLResponse)
async def new_line_form(request: Request):
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "line_form.html",
        {
            "request": request,
            "line": None,
            "cities": cities,
            "categories": categories,
        },
    )


@app.get("/admin/lines/{line_id}/edit", response_class=HTMLResponse)
async def edit_line_form(request: Request, line_id: int):
    line = db.get_line(line_id)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "line_form.html",
        {
            "request": request,
            "line": line,
            "cities": cities,
            "categories": categories,
        },
    )


@app.post("/admin/lines")
async def create_line(
    line_number: str = Form(...),
    description: str = Form(""),
    status: str = Form("active"),
    gauge_type: str = Form(None),
    cities_served: str = Form(""),
    category_id: int = Form(None),
):
    cities = (
        [city.strip() for city in cities_served.split(",") if city.strip()]
        if cities_served
        else []
    )
    line_data = LineCreate(
        line_number=line_number,
        description=description,
        status=status,
        gauge_type=gauge_type if gauge_type else None,
        cities_served=cities,
        category_id=category_id,
    )
    line = db.create_line(line_data)
    return RedirectResponse(url=f"/lines/{line.id}", status_code=303)


@app.post("/admin/lines/{line_id}")
async def update_line(
    line_id: int,
    line_number: str = Form(...),
    description: str = Form(""),
    status: str = Form("active"),
    gauge_type: str = Form(None),
    cities_served: str = Form(""),
    category_id: int = Form(None),
):
    cities = (
        [city.strip() for city in cities_served.split(",") if city.strip()]
        if cities_served
        else []
    )
    line_data = LineUpdate(
        line_number=line_number,
        description=description,
        status=status,
        gauge_type=gauge_type if gauge_type else None,
        cities_served=cities,
        category_id=category_id,
    )
    line = db.update_line(line_id, line_data)
    if not line:
        raise HTTPException(status_code=404, detail="Line not found")
    return RedirectResponse(url=f"/lines/{line.id}", status_code=303)


@app.post("/admin/lines/{line_id}/delete")
async def delete_line(line_id: int):
    success = db.delete_line(line_id)
    if not success:
        raise HTTPException(status_code=404, detail="Line not found")
    return RedirectResponse(url="/lines", status_code=303)


# Form Routes - Stations
@app.get("/admin/stations/new", response_class=HTMLResponse)
async def new_station_form(request: Request):
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "station_form.html",
        {
            "request": request,
            "station": None,
            "cities": cities,
            "categories": categories,
        },
    )


@app.get("/admin/stations/{station_id}/edit", response_class=HTMLResponse)
async def edit_station_form(request: Request, station_id: int):
    station = db.get_station(station_id)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "station_form.html",
        {
            "request": request,
            "station": station,
            "cities": cities,
            "categories": categories,
        },
    )


@app.post("/admin/stations")
async def create_station(
    station_code: str = Form(...),
    name: str = Form(...),
    address: str = Form(...),
    services: str = Form(""),
    accessibility: str = Form(""),
    station_type: Optional[str] = Form(None),
    province: Optional[str] = Form(None),
    city_id: Optional[int] = Form(None),
):
    services_list = (
        [service.strip() for service in services.split(",") if service.strip()]
        if services
        else []
    )
    accessibility_list = (
        [access.strip() for access in accessibility.split(",") if access.strip()]
        if accessibility
        else []
    )
    station_data = StationCreate(
        station_code=station_code,
        name=name,
        address=address,
        services=services_list,
        accessibility=accessibility_list,
        station_type=station_type if station_type else None,
        province=province if province else None,
        city_id=city_id,
    )
    station = db.create_station(station_data)
    return RedirectResponse(url=f"/stations/{station.id}", status_code=303)


@app.post("/admin/stations/{station_id}")
async def update_station(
    station_id: int,
    station_code: str = Form(...),
    name: str = Form(...),
    address: str = Form(...),
    services: str = Form(""),
    accessibility: str = Form(""),
    station_type: Optional[str] = Form(None),
    province: Optional[str] = Form(None),
    city_id: Optional[int] = Form(None),
):
    services_list = (
        [service.strip() for service in services.split(",") if service.strip()]
        if services
        else []
    )
    accessibility_list = (
        [access.strip() for access in accessibility.split(",") if access.strip()]
        if accessibility
        else []
    )
    station_data = StationUpdate(
        station_code=station_code,
        name=name,
        address=address,
        services=services_list,
        accessibility=accessibility_list,
        station_type=station_type if station_type else None,
        province=province if province else None,
        city_id=city_id,
    )
    station = db.update_station(station_id, station_data)
    if not station:
        raise HTTPException(status_code=404, detail="Station not found")
    return RedirectResponse(url=f"/stations/{station.id}", status_code=303)


@app.post("/admin/stations/{station_id}/delete")
async def delete_station(station_id: int):
    success = db.delete_station(station_id)
    if not success:
        raise HTTPException(status_code=404, detail="Station not found")
    return RedirectResponse(url="/stations", status_code=303)


# Form Routes - Projects
@app.get("/admin/projects/new", response_class=HTMLResponse)
async def new_project_form(request: Request):
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "project_form.html",
        {
            "request": request,
            "project": None,
            "cities": cities,
            "categories": categories,
        },
    )


@app.get("/admin/projects/{project_id}/edit", response_class=HTMLResponse)
async def edit_project_form(request: Request, project_id: int):
    project = db.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    cities = db.get_cities()
    categories = db.get_categories()
    return templates.TemplateResponse(
        "project_form.html",
        {
            "request": request,
            "project": project,
            "cities": cities,
            "categories": categories,
        },
    )


@app.post("/admin/projects")
async def create_project(
    title: str = Form(...),
    description: str = Form(...),
    project_type: str = Form(...),
    budget: float = Form(None),
    timeline: str = Form(""),
    status: str = Form("planning"),
    city_id: int = Form(None),
    category_id: int = Form(None),
):
    project_data = ProjectCreate(
        title=title,
        description=description,
        project_type=project_type,
        budget=budget,
        timeline=timeline,
        status=status,
        city_id=city_id,
        category_id=category_id,
    )
    project = db.create_project(project_data)
    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@app.post("/admin/projects/{project_id}")
async def update_project(
    project_id: int,
    title: str = Form(...),
    description: str = Form(...),
    project_type: str = Form(...),
    budget: float = Form(None),
    timeline: str = Form(""),
    status: str = Form("planning"),
    city_id: int = Form(None),
    category_id: int = Form(None),
):
    project_data = ProjectUpdate(
        title=title,
        description=description,
        project_type=project_type,
        budget=budget,
        timeline=timeline,
        status=status,
        city_id=city_id,
        category_id=category_id,
    )
    project = db.update_project(project_id, project_data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return RedirectResponse(url=f"/projects/{project.id}", status_code=303)


@app.post("/admin/projects/{project_id}/delete")
async def delete_project(project_id: int):
    success = db.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return RedirectResponse(url="/projects", status_code=303)


# Form Routes - Events
@app.get("/admin/events/new", response_class=HTMLResponse)
async def new_event_form(request: Request):
    cities = db.get_cities()
    lineas = db.get_lines()
    return templates.TemplateResponse(
        "event_form.html",
        {
            "request": request,
            "event": None,
            "ciudades": cities,
            "lineas": lineas,
        },
    )


@app.get("/admin/events/{event_id}/edit", response_class=HTMLResponse)
async def edit_event_form(request: Request, event_id: int):
    event = db.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    cities = db.get_cities()
    lineas = db.get_lines()
    return templates.TemplateResponse(
        "event_form.html",
        {
            "request": request,
            "event": event,
            "ciudades": cities,
            "lineas": lineas,
        },
    )


@app.post("/admin/events")
async def create_event(
    title: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(""),
    location: str = Form(...),
    event_type: str = Form(...),
    city_id: int = Form(None),
):
    from datetime import datetime

    event_data = EventCreate(
        title=title,
        description=description,
        event_date=datetime.strptime(event_date, "%Y-%m-%d"),
        event_time=event_time,
        location=location,
        event_type=event_type,
        city_id=city_id,
    )
    event = db.create_event(event_data)
    return RedirectResponse(url="/posts/eventos", status_code=303)


@app.post("/admin/events/{event_id}")
async def update_event(
    event_id: int,
    title: str = Form(...),
    description: str = Form(...),
    event_date: str = Form(...),
    event_time: str = Form(""),
    location: str = Form(...),
    event_type: str = Form(...),
    city_id: int = Form(None),
):
    from datetime import datetime

    event_data = EventUpdate(
        title=title,
        description=description,
        event_date=datetime.strptime(event_date, "%Y-%m-%d"),
        event_time=event_time,
        location=location,
        event_type=event_type,
        city_id=city_id,
    )
    event = db.update_event(event_id, event_data)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return RedirectResponse(url="/posts/eventos", status_code=303)


@app.post("/admin/events/{event_id}/delete")
async def delete_event(event_id: int):
    success = db.delete_event(event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")
    return RedirectResponse(url="/posts/eventos", status_code=303)


# Form Routes - Cities
@app.get("/admin/cities/new", response_class=HTMLResponse)
async def new_city_form(request: Request):
    return templates.TemplateResponse(
        "city_form.html",
        {
            "request": request,
            "city": None,
        },
    )


@app.get("/admin/cities/{city_id}/edit", response_class=HTMLResponse)
async def edit_city_form(request: Request, city_id: int):
    city = db.get_city(city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return templates.TemplateResponse(
        "city_form.html",
        {
            "request": request,
            "city": city,
        },
    )


@app.post("/admin/cities")
async def create_city(
    name: str = Form(...),
    slug: str = Form(...),
    region: str = Form(""),
    country: str = Form("Spain"),
):
    city_data = CityCreate(
        name=name,
        slug=slug,
        region=region,
        country=country,
    )
    city = db.create_city(city_data)
    return RedirectResponse(url=f"/cities/{city.slug}", status_code=303)


@app.post("/admin/cities/{city_id}")
async def update_city(
    city_id: int,
    name: str = Form(...),
    slug: str = Form(...),
    region: str = Form(""),
    country: str = Form("Spain"),
):
    city_data = CityUpdate(
        name=name,
        slug=slug,
        region=region,
        country=country,
    )
    city = db.update_city(city_id, city_data)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return RedirectResponse(url=f"/cities/{city.slug}", status_code=303)


@app.post("/admin/cities/{city_id}/delete")
async def delete_city(city_id: int):
    success = db.delete_city(city_id)
    if not success:
        raise HTTPException(status_code=404, detail="City not found")
    return RedirectResponse(url="/cities", status_code=303)


# Form Routes - Categories
@app.get("/admin/categories/new", response_class=HTMLResponse)
async def new_category_form(request: Request):
    categories = db.get_categories()
    return templates.TemplateResponse(
        "category_form.html",
        {
            "request": request,
            "category": None,
            "categorias": categories,
        },
    )


@app.get("/admin/categories/{category_id}/edit", response_class=HTMLResponse)
async def edit_category_form(request: Request, category_id: int):
    category = db.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    categories = db.get_categories()
    return templates.TemplateResponse(
        "category_form.html",
        {
            "request": request,
            "category": category,
            "categorias": categories,
        },
    )


@app.post("/admin/categories")
async def create_category(
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(""),
    parent_id: int = Form(None),
):
    category_data = CategoryCreate(
        name=name,
        slug=slug,
        description=description,
        parent_id=parent_id,
    )
    category = db.create_category(category_data)
    return RedirectResponse(url=f"/categories/{category.id}", status_code=303)


@app.post("/admin/categories/{category_id}")
async def update_category(
    category_id: int,
    name: str = Form(...),
    slug: str = Form(...),
    description: str = Form(""),
    parent_id: int = Form(None),
):
    category_data = CategoryUpdate(
        name=name,
        slug=slug,
        description=description,
        parent_id=parent_id,
    )
    category = db.update_category(category_id, category_data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return RedirectResponse(url=f"/categories/{category.id}", status_code=303)


@app.post("/admin/categories/{category_id}/delete")
async def delete_category(category_id: int):
    success = db.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return RedirectResponse(url="/categories", status_code=303)


# Admin listing routes for railway entities
@app.get("/admin/lines", response_class=HTMLResponse)
async def admin_list_lines(request: Request):
    try:
        lines = db.get_lines()
    except:
        lines = []
    return templates.TemplateResponse(
        "admin_lines.html",
        {
            "request": request,
            "lines": lines,
        },
    )


@app.get("/admin/stations", response_class=HTMLResponse)
async def admin_list_stations(request: Request):
    try:
        stations = db.get_stations()
    except:
        stations = []
    return templates.TemplateResponse(
        "admin_stations.html",
        {
            "request": request,
            "stations": stations,
        },
    )


@app.get("/admin/projects", response_class=HTMLResponse)
async def admin_list_projects(request: Request):
    try:
        projects = db.get_projects()
    except:
        projects = []
    return templates.TemplateResponse(
        "admin_projects.html",
        {
            "request": request,
            "projects": projects,
        },
    )


@app.get("/admin/events", response_class=HTMLResponse)
async def admin_list_events(request: Request):
    try:
        events = db.get_events()
    except:
        events = []
    return templates.TemplateResponse(
        "admin_events.html",
        {
            "request": request,
            "events": events,
        },
    )


@app.get("/admin/cities", response_class=HTMLResponse)
async def admin_list_cities(request: Request):
    try:
        cities = db.get_cities()
    except:
        cities = []
    return templates.TemplateResponse(
        "admin_cities.html",
        {
            "request": request,
            "cities": cities,
        },
    )


@app.get("/admin/categories", response_class=HTMLResponse)
async def admin_list_categories(request: Request):
    try:
        categories = db.get_categories()
    except:
        categories = []
    return templates.TemplateResponse(
        "admin_categories.html",
        {
            "request": request,
            "categories": categories,
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=4444)
