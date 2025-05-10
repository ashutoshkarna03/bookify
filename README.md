# Bookify

Bookify is a modern book management API built with FastAPI and Strawberry GraphQL, using SQLAlchemy and PostgreSQL for data storage. It supports both REST and GraphQL endpoints, and is ready for production with environment-based configuration and database migrations via Alembic.

## Features

- FastAPI REST API
- GraphQL API using Strawberry
- SQLAlchemy ORM models for Book and Author
- PostgreSQL database support
- Alembic migrations
- Environment-based configuration with `.env`
- Ready for Docker deployment (optional)

## Project Structure

```
bookify/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── graphql/
│       ├── __init__.py
│       └── schema.py
├── alembic/
│   └── versions/
├── alembic.ini
├── requirements.txt
├── .env
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd bookify
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/bookify
ENVIRONMENT=development
DEBUG=True
```

Adjust the `DATABASE_URL` as needed for your setup.

### 5. Set up the database

Make sure PostgreSQL is running and the database exists. Then run:

```bash
alembic upgrade head
```

This will apply the latest migrations and create the necessary tables.

### 6. Run the application

```bash
uvicorn app.main:app --reload
```

- REST API: [http://localhost:8000](http://localhost:8000)
- GraphQL Playground: [http://localhost:8000/graphql](http://localhost:8000/graphql)

## Example GraphQL Query

```graphql
query {
  books {
    id
    title
    description
    author {
      id
      name
    }
  }
}
```

## Development

- To create a new migration after changing models:
  ```bash
  alembic revision --autogenerate -m "Describe your change"
  alembic upgrade head
  ```
- To run tests (add your tests and use pytest):
  ```bash
  pytest
  ```

## License

MIT
