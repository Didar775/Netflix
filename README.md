# Netflix API

FastAPI application for managing movies and users.

## Setup

### Using Docker Compose

1. Build and start the application with Docker Compose:
```bash
docker-compose up --build
```

Or to run in detached mode:
```bash
docker-compose up --build -d
```

The application will be available at http://localhost:8000

### Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --reload
```

## Data Loading

The repository includes a CSV file (`app/services/netflix.csv`) containing movie data. When the project starts up, this data is automatically loaded into the database if the database is empty. Once loaded, all movie data is available through the API endpoints.

## Authentication

The API includes authorization logic. To access movie endpoints, you must first authenticate:

1. **Register** a new user at `/auth/register`
2. **Login** at `/auth/login` to receive an access token
3. Use the access token in the Authorization header when making requests to movie endpoints

All movie endpoints (`/movies/*`) require authentication. Include the token in the request header:
```
Authorization: Bearer <your_access_token>
```

## API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Use the `/docs` endpoint to interact with the API interface.

