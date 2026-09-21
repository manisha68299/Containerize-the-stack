# Containerize the Stack

A containerized **FastAPI + PostgreSQL Task Management API** built to demonstrate REST API development, database integration, Docker, and Docker Compose.

The application consists of two containers:

* **FastAPI** — REST API running on port `3000`
* **PostgreSQL** — relational database running on port `5432`

Docker Compose manages both services and connects them through the internal Docker network.

---

## Tech Stack

| Technology     | Purpose                       |
| -------------- | ----------------------------- |
| Python 3.12    | Backend runtime               |
| FastAPI        | REST API framework            |
| Uvicorn        | ASGI server                   |
| PostgreSQL 16  | Relational database           |
| Psycopg        | PostgreSQL driver             |
| Docker         | Containerization              |
| Docker Compose | Multi-container orchestration |

---

## Features

* RESTful API using FastAPI
* PostgreSQL database integration
* Create, read, update, and delete tasks
* Automatic database initialization
* Automatic `tasks` table creation
* Sample task insertion on first startup
* PostgreSQL connection retry mechanism
* Dockerized FastAPI application
* Dockerized PostgreSQL database
* Docker Compose orchestration
* Persistent PostgreSQL storage using a Docker volume
* Swagger/OpenAPI documentation
* Pydantic request validation

---

## Architecture

```text
                         Docker Compose
                              |
                +-------------+-------------+
                |                           |
                v                           v
        FastAPI Container           PostgreSQL Container
           Port 3000                    Port 5432
                |                           |
                +-----------+---------------+
                            |
                     Docker Network
                            |
                     PostgreSQL DB
```

Application flow:

```text
Client
   |
   | HTTP
   v
FastAPI
   |
   | SQL
   v
PostgreSQL
   |
   v
postgres_data volume
```

---

# Project Structure

```text
Containerize-the-stack/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI routes and validation
│   └── repository.py        # PostgreSQL connection and SQL logic
│
├── .env                     # Local environment variables
├── .env.example             # Environment variable template
├── .gitignore
├── Dockerfile               # FastAPI image definition
├── compose.yaml             # FastAPI + PostgreSQL services
├── requirements.txt         # Python dependencies
└── README.md
```

---

# Prerequisites

Install:

* Docker Desktop
* Git

Verify Docker:

```powershell
docker --version
docker compose version
docker ps
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
DB_USER=postgres
DB_PASSWORD=dev
DB_NAME=Flyrank
DATABASE_URL=postgresql://postgres:dev@db:5432/Flyrank
```

### Important

Inside Docker Compose, the PostgreSQL hostname is:

```text
db
```

Do **not** use:

```text
localhost
```

for the API's PostgreSQL connection.

`localhost` inside the FastAPI container refers to the FastAPI container itself.

Docker Compose provides service-to-service communication using the service name:

```text
db
```

---

# Startup Workflow

The entire application can be started with Docker Compose.

## 1. Clone the Repository

```powershell
git clone https://github.com/manisha68299/Containerize-the-stack.git
cd Containerize-the-stack
```

---

## 2. Create `.env`

If `.env.example` exists:

```powershell
Copy-Item .env.example .env
```

Check the configuration:

```powershell
Get-Content .env
```

Expected configuration:

```env
DB_USER=postgres
DB_PASSWORD=dev
DB_NAME=Flyrank
DATABASE_URL=postgresql://postgres:dev@db:5432/Flyrank
```

---

## 3. Build and Start the Stack

Run:

```powershell
docker compose up --build -d
```

This command:

1. Builds the FastAPI image.
2. Pulls the PostgreSQL image if necessary.
3. Creates the Docker network.
4. Starts PostgreSQL.
5. Starts FastAPI.
6. Creates the PostgreSQL volume.
7. Runs both services in detached mode.

---

## 4. Check the Services

```powershell
docker compose ps
```

Expected services:

```text
api
db
```

You can also check all running containers:

```powershell
docker ps
```

---

# Access the Application

## API

Open:

```text
http://localhost:3000/tasks
```

## Swagger UI

Open:

```text
http://localhost:3000/docs
```

Swagger provides an interactive interface for testing the API.

---

# API Endpoints

| Method | Endpoint           | Description           |
| ------ | ------------------ | --------------------- |
| GET    | `/tasks`           | Get all tasks         |
| GET    | `/tasks/{task_id}` | Get one task          |
| POST   | `/tasks`           | Create a task         |
| PUT    | `/tasks/{task_id}` | Update a task         |
| DELETE | `/tasks/{task_id}` | Delete a task         |
| GET    | `/docs`            | Swagger documentation |

---

# Testing the API

## Get All Tasks

```powershell
curl.exe -i http://localhost:3000/tasks
```

PowerShell alternative:

```powershell
Invoke-RestMethod http://localhost:3000/tasks
```

Example response:

```json
[
  {
    "id": 1,
    "title": "Learn Docker",
    "done": false
  },
  {
    "id": 2,
    "title": "Connect PostgreSQL",
    "done": false
  },
  {
    "id": 3,
    "title": "Build a task API",
    "done": false
  }
]
```

---

## Get One Task

```powershell
curl.exe -i http://localhost:3000/tasks/1
```

Example:

```json
{
  "id": 1,
  "title": "Learn Docker",
  "done": false
}
```

---

## Get a Non-Existing Task

```powershell
curl.exe -i http://localhost:3000/tasks/999
```

Response:

```json
{
  "error": "Task not found"
}
```

---

# Create a Task

```powershell
curl.exe -i -X POST http://localhost:3000/tasks `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"Learn Docker\",\"done\":false}"
```

Example response:

```json
{
  "id": 4,
  "title": "Learn Docker",
  "done": false
}
```

---

# Update a Task

```powershell
curl.exe -i -X PUT http://localhost:3000/tasks/1 `
  -H "Content-Type: application/json" `
  -d "{\"title\":\"Learn PostgreSQL\",\"done\":true}"
```

Example response:

```json
{
  "id": 1,
  "title": "Learn PostgreSQL",
  "done": true
}
```

---

# Delete a Task

```powershell
curl.exe -i -X DELETE http://localhost:3000/tasks/1
```

Successful deletion returns:

```text
204 No Content
```

---

# Database

PostgreSQL runs as the `db` service.

The database configuration is:

```env
DB_USER=postgres
DB_PASSWORD=dev
DB_NAME=Flyrank
```

The API connects using:

```text
postgresql://postgres:dev@db:5432/Flyrank
```

---

# Check PostgreSQL

## Check Database Health

```powershell
docker compose exec db pg_isready -U postgres -d Flyrank
```

Expected:

```text
accepting connections
```

---

## List Tables

```powershell
docker compose exec db psql -U postgres -d Flyrank -c "\dt"
```

---

## View Tasks

```powershell
docker compose exec db psql -U postgres -d Flyrank -c "SELECT * FROM tasks;"
```

---

## Open PostgreSQL Shell

```powershell
docker compose exec db psql -U postgres -d Flyrank
```

Inside PostgreSQL:

```sql
\dt
```

View tasks:

```sql
SELECT * FROM tasks;
```

Exit:

```sql
\q
```

---

# Logs

## View All Logs

```powershell
docker compose logs
```

## Follow All Logs

```powershell
docker compose logs -f
```

## API Logs

```powershell
docker compose logs api
```

## Database Logs

```powershell
docker compose logs db
```

## Follow API Logs

```powershell
docker compose logs -f api
```

Press `Ctrl+C` to stop viewing logs.

The containers continue running because they were started with `-d`.

---

# Database Persistence

PostgreSQL uses a named Docker volume:

```text
postgres_data
```

This volume keeps database data even when the containers are stopped.

Test persistence:

### Stop the stack

```powershell
docker compose down
```

### Start it again

```powershell
docker compose up -d
```

### Check the tasks

```powershell
curl.exe -i http://localhost:3000/tasks
```

Previously created tasks should still exist.

---

# Stop the Application

Stop and remove the containers:

```powershell
docker compose down
```

The PostgreSQL volume is preserved.

---

# Delete the Database

If you want to completely remove the database and all stored tasks:

```powershell
docker compose down -v
```

> **Warning:** `-v` removes the PostgreSQL Docker volume and permanently deletes the stored database data.

Start with a fresh database:

```powershell
docker compose up --build -d
```

---

# Rebuild After Code Changes

After modifying Python code or dependencies:

```powershell
docker compose down
docker compose up --build -d
```

Check the services:

```powershell
docker compose ps
```

Test the API:

```powershell
curl.exe -i http://localhost:3000/tasks
```

---

# Troubleshooting

## API Is Not Working

Check the containers:

```powershell
docker compose ps -a
```

Check API logs:

```powershell
docker compose logs api
```

Check database logs:

```powershell
docker compose logs db
```

Restart the complete stack:

```powershell
docker compose down
docker compose up --build -d
```

---

## API Cannot Connect to PostgreSQL

Check PostgreSQL:

```powershell
docker compose exec db pg_isready -U postgres -d Flyrank
```

Make sure the API uses:

```text
db
```

as the database hostname:

```text
postgresql://postgres:dev@db:5432/Flyrank
```

Do not use:

```text
postgresql://postgres:dev@localhost:5432/Flyrank
```

inside the API container.

---

## Port 3000 Is Already in Use

Change the host port in `compose.yaml`.

For example:

```yaml
ports:
  - "3001:3000"
```

Then restart:

```powershell
docker compose down
docker compose up --build -d
```

The API will then be available at:

```text
http://localhost:3001/tasks
```

---

## Port 5432 Is Already in Use

Check running containers:

```powershell
docker ps
```

A PostgreSQL installation running directly on Windows may already be using port `5432`.

Stop the conflicting service or change the PostgreSQL host port in `compose.yaml`.

---

# Normal Daily Workflow

For normal development, only these commands are required.

### Start

```powershell
docker compose up --build -d
```

### Check

```powershell
docker compose ps
```

### Test

```powershell
curl.exe -i http://localhost:3000/tasks
```

### View Logs

```powershell
docker compose logs -f
```

### Stop

```powershell
docker compose down
```

---

# Full Clean Restart

Use this only when you want to delete the existing database and start completely fresh:

```powershell
docker compose down -v
docker compose up --build -d
docker compose ps
curl.exe -i http://localhost:3000/tasks
```

---

# Docker Command Reference

| Command                                 | Purpose                            |
| --------------------------------------- | ---------------------------------- |
| `docker compose up -d`                  | Start the stack                    |
| `docker compose up --build -d`          | Build and start the stack          |
| `docker compose down`                   | Stop and remove containers         |
| `docker compose down -v`                | Stop containers and delete volumes |
| `docker compose ps`                     | Show Compose services              |
| `docker compose logs`                   | Show logs                          |
| `docker compose logs -f`                | Follow logs                        |
| `docker compose logs api`               | Show API logs                      |
| `docker compose logs db`                | Show database logs                 |
| `docker compose exec db psql ...`       | Open PostgreSQL                    |
| `docker compose exec db pg_isready ...` | Check PostgreSQL health            |

---

# What This Project Demonstrates

This project demonstrates practical experience with:

* Python backend development
* FastAPI
* REST API design
* PostgreSQL
* SQL CRUD operations
* Database connection management
* Pydantic validation
* Dockerfiles
* Docker images
* Docker containers
* Docker Compose
* Container networking
* Environment variables
* Docker volumes
* Database persistence
* Swagger/OpenAPI
* API testing
* Docker troubleshooting

---

# Author

**Manisha Banerjee**

GitHub: [github.com/manisha68299](https://github.com/manisha68299)

Repository: [Containerize-the-stack](https://github.com/manisha68299/Containerize-the-stack)
