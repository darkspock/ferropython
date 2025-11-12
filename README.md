# FastAPI Blog

A simple blog application built with FastAPI, featuring both web interface and REST API.

## Features

- Create, read, update, and delete blog posts
- Responsive web interface with HTML templates
- REST API endpoints for programmatic access
- Clean, modern CSS styling
- In-memory data storage (for simplicity)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up MySQL database and update `.env` file with your credentials

3. Run database migrations:
```bash
alembic upgrade head
```

4. Run the application:
```bash
python main.py
```

5. Open your browser and navigate to `http://localhost:4444`

## Database Migrations

To create new migrations after model changes:
```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

To rollback migrations:
```bash
alembic downgrade -1
```

## API Endpoints

- `GET /api/posts` - Get all posts
- `GET /api/posts/{id}` - Get a specific post
- `POST /api/posts` - Create a new post
- `PUT /api/posts/{id}` - Update a post
- `DELETE /api/posts/{id}` - Delete a post

## Web Interface

- `/` - Home page with all posts
- `/post/{id}` - View a single post
- `/new` - Create a new post
- `/edit/{id}` - Edit an existing post

## Project Structure

```
blogp/
├── main.py              # FastAPI application
├── models.py            # Pydantic models
├── database.py          # In-memory database
├── requirements.txt     # Python dependencies
├── templates/           # HTML templates
│   ├── index.html
│   ├── post.html
│   ├── new_post.html
│   └── edit_post.html
└── static/              # CSS files
    └── style.css
```

## Usage

1. Start the server with `python main.py`
2. Visit `http://localhost:8000` to see the blog
3. Click "New Post" to create your first blog post
4. Use the API endpoints to interact with the blog programmatically

The blog uses an in-memory database, so data will be lost when the server restarts. For production use, you would want to integrate a persistent database like PostgreSQL or SQLite.