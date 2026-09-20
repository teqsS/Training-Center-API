# Training Center API

An asynchronous REST API for managing students, courses, and enrollments at a training center. The project focuses on explicit business rules, PostgreSQL-backed data integrity, application-level resource ownership, integration tests, and continuous integration.

**Current version: `0.1.0`.** This is a working educational/portfolio project, not a publicly deployed production service. Authentication, application containerization, deployment automation, and operational monitoring are not implemented yet.

## Features

- Create, retrieve, and partially update students and courses. DELETE deactivates them instead of removing their rows.
- Enroll an active student in an active course, subject to course capacity.
- Allow at most one **active** enrollment per student/course pair. PostgreSQL enforces this with a partial unique index.
- Count only active enrollments against a course's capacity. The course row is locked before counting and inserting, so concurrent requests serialize on the same course.
- Complete or cancel an active enrollment. Terminal states cannot transition again; a student can enroll in the same course after an earlier enrollment is completed or cancelled.
- List the active students of a course and the active courses of a student.
- Return domain-specific `404` and `409` responses; validate input with Pydantic and expose an OpenAPI schema.

## Tech stack

| Area | Technology |
| --- | --- |
| API and validation | Python 3.14, FastAPI, Pydantic v2, pydantic-settings |
| Persistence | PostgreSQL 17, SQLAlchemy 2.x async ORM, asyncpg, Alembic |
| Tooling | uv, pytest, pytest-asyncio, Ruff, mypy |
| CI | GitHub Actions with a temporary PostgreSQL service |

## Architecture

```text
HTTP request
→ router: endpoint and input/output DTOs
→ service: business rules and transaction boundaries
→ repository: SQLAlchemy queries
→ PostgreSQL: constraints, indexes, and persisted data
```

`create_app()` constructs a FastAPI instance. During its lifespan, each application instance receives its own asynchronous engine and session factory; the engine is disposed of on shutdown. A request dependency provides an `AsyncSession`. Pydantic defines the public input contract, services coordinate domain operations, and database constraints provide a final integrity boundary.

```text
src/main.py ASGI entry point
src/app/application.py app factory and lifespan
src/app/config.py environment-based settings
src/app/routers/ HTTP endpoints
src/app/schemas/ Pydantic DTOs
src/app/services/ business logic
src/app/repositories/ database queries
src/app/models/ ORM models and constraints
src/app/dependencies/ database session dependency
src/app/migrations/ Alembic migrations
tests/ smoke and PostgreSQL integration tests
.github/workflows/ci.yml GitHub Actions quality gate
```

### Data model and business rules

| Entity | Main fields | Rules |
| --- | --- | --- |
| Student | name, unique email, age (16–100), skills | `is_active` is system-managed; deactivated students are excluded from active lookups |
| Course | name, teacher, optional description, price, capacity, level | capacity is 1–500 (default 100); level defaults to `beginner`; deactivated courses are excluded from active lookups |
| Enrollment | student ID, course ID, status, timestamps | starts as `active`; valid transitions are `active → completed` and `active → cancelled`; only active enrollments occupy seats |

Completed and cancelled enrollments remain in the database as history. Enrollment timestamps use PostgreSQL `timestamp with time zone`; SQLAlchemy updates `updated_at` when the row changes. System-managed fields such as IDs, activation flags, enrollment status, and timestamps are not accepted in create requests.

## Run locally

You need [uv](https://docs.astral.sh/uv/getting-started/installation/), Python 3.14, and an accessible PostgreSQL instance. The example below uses PostgreSQL 17 in Docker; the API itself runs on your host. If PostgreSQL already runs locally or on a VM, use that instance and set the corresponding connection variables.

1. Install the locked dependencies from the repository root:

   ```bash
   uv sync --locked --dev
   ```

2. If needed, start a **local-development-only** PostgreSQL container:

   ```bash
   docker run -d --name training-center-postgres \
   -p 127.0.0.1:5432:5432 \
   --mount type=volume,src=training-center-pgdata,dst=/var/lib/postgresql/data \
   -e POSTGRES_USER=training_center \
   -e POSTGRES_PASSWORD=local-demo-only \
   -e POSTGRES_DB=training_center \
   postgres:17-alpine
   ```

   If port 5432 is occupied, change the published port and `DB_PORT` accordingly. An existing PostgreSQL installation also needs a dedicated user and database.

3. Create a local configuration file:

   ```bash
   cp .env.example .env
   ```

   For the container above, set:

   ```dotenv
   DB_USER=training_center
   DB_PASS=local-demo-only
   DB_HOST=127.0.0.1
   DB_PORT=5432
   DB_NAME=training_center
   ```

   `.env` is ignored by Git. Do not use the example password for any externally accessible deployment. When PostgreSQL runs on a VM, `DB_HOST` must be an address reachable from the machine running the API, not an internal container address.

4. Apply migrations and start the API:

   ```bash
   uv run alembic upgrade head
   uv run uvicorn main:app --app-dir src --host 127.0.0.1 --port 8000
   ```

5. Open [Swagger UI](http://127.0.0.1:8000/docs), [OpenAPI JSON](http://127.0.0.1:8000/openapi.json), or `GET http://127.0.0.1:8000/training_center_api/`.

The system endpoint indicates that the process responds; it **does not verify PostgreSQL connectivity**. A database readiness probe has not been added yet.

### Example API flow

Create a course. Omitted `capacity` and `level` use their defaults:

```bash
curl -X POST http://127.0.0.1:8000/training_center_api/courses/ \
-H 'Content-Type: application/json' \
-d '{"name":"Python Backend","teacher":"Alex Morgan","price":20000}'
```

Create a student:

```bash
curl -X POST http://127.0.0.1:8000/training_center_api/students/ \
-H 'Content-Type: application/json' \
-d '{"full_name":"Sam Taylor","email":"sam@example.com","age":21,"skills":["python"]}'
```

Use the IDs returned by those requests. The following IDs are examples:

```bash
curl -X POST http://127.0.0.1:8000/training_center_api/enrollments/ \
-H 'Content-Type: application/json' \
-d '{"student_id":1,"course_id":1}'
```

The response includes an ID, `status: "active"`, `created_at`, and `updated_at`. Repeating the same active enrollment returns `409 Conflict`. Complete it with `PATCH /training_center_api/enrollments/{id}/complete` or cancel it with `DELETE /training_center_api/enrollments/{id}`.

## API overview

All paths below have the `/training_center_api` prefix. For exact request bodies, response schemas, and interactive examples, visit `/docs`.

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/` | Process information |
| GET | `/students`, `/students/{id}` | List active students / get an active student |
| POST | `/students/` | Create a student |
| PATCH, DELETE | `/students/{id}` | Partially update / deactivate a student |
| GET | `/students/{id}/courses` | Active courses for a student |
| GET | `/courses`, `/courses/{id}` | List active courses / get an active course |
| POST | `/courses/` | Create a course |
| PATCH, DELETE | `/courses/{id}` | Partially update / deactivate a course |
| GET | `/courses/{id}/students` | Active students in a course |
| POST | `/enrollments/` | Enroll a student in a course |
| PATCH | `/enrollments/{id}/complete` | Complete an active enrollment |
| DELETE | `/enrollments/{id}` | Cancel an active enrollment (no physical deletion) |

PATCH uses only explicitly provided fields (`exclude_unset=True`). Unknown fields are forbidden in create requests. Domain errors use `{"detail": "..."}`; FastAPI returns `422` for input validation failures.

## Tests and continuous integration

Integration tests require a **separate** PostgreSQL database whose name starts with `test_`. Before and after each database-backed test, the fixture runs `TRUNCATE ... RESTART IDENTITY CASCADE` on `courses`, `students`, and `enrollments`. **Never point the test suite at a database containing valuable data.**

For the example container, create a test database:

```bash
docker exec training-center-postgres \
psql -U training_center -d postgres -c 'CREATE DATABASE test_training_center;'
```

Apply migrations to that test database and run the checks from the repository root. The inline `DB_NAME` value applies only to its individual command; all other settings come from `.env` or the environment:

```bash
DB_NAME=test_training_center uv run alembic upgrade head
DB_NAME=test_training_center uv run alembic check
DB_NAME=test_training_center uv run pytest tests
uv run ruff check .
uv run ruff format --check .
uv run mypy src tests
uv build
```

For a PostgreSQL server on a VM or with other credentials, provide the appropriate `DB_USER`, `DB_PASS`, `DB_HOST`, `DB_PORT`, and `DB_NAME` values. Keep real secrets out of Git. `alembic check` compares migration state with the current ORM metadata.

The GitHub Actions workflow runs for pull requests targeting `main` and pushes to `main`. It starts a temporary PostgreSQL 17 service, applies and checks migrations, runs Ruff, mypy, and pytest, then builds the Python package. This is **CI, not automated deployment**.

## Current limitations and roadmap

- No authentication or authorization. **Do not expose write endpoints to the public Internet with real data.**
- No application Docker image, Compose setup, or public deployment yet.
- The `/statistics` router is a placeholder and currently has no endpoints.
- The system endpoint is not a database readiness check.
- Row locks are used for capacity checks and status transitions; dedicated concurrent integration tests are still planned.
- Operating with real data additionally requires HTTPS, secret management, backup and restore verification, monitoring, and deployment/rollback procedures.
Next steps: containerize the application, establish a verified deployment workflow, add operational documentation, and secure the API. This README documents the **current implementation**, not an already existing production environment.
