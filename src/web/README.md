# arXiv Full-Stack Application

A full-stack application for parsing and summarizing arXiv papers, built with Next.js (React) frontend and Python FastAPI backend following Domain-Driven Design (DDD) architecture.

## Architecture

- **Frontend**: Next.js (React) with TypeScript and SCSS
- **Backend**: Python FastAPI with DDD architecture (Domain, Application, Infrastructure, Presentation layers)
- **Database**: SQLite for local development, PostgreSQL for production (via Docker Compose)
- **Containerization**: Docker Compose for easy deployment

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm
- Docker and Docker Compose (for containerized setup)
- PostgreSQL 15+ (only needed for Docker Compose setup; local development uses SQLite)
- Local LLM server (optional, for paper summarization)

## Quick Start with Docker Compose

The easiest way to run the entire application:

```bash
# From the project root directory
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Backend API on port 8000
- Database migrations will run automatically

Then start the frontend:

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Manual Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure settings:**
   **IMPORTANT:** You must create and configure `config/config.yaml` with required settings.
   The application will not start without proper database configuration.
   
   Edit `config/config.yaml` to configure:
   - **Database type and URL (REQUIRED)**
   - LLM provider settings:
   ```yaml
   database:
     # Database type: "sqlite" or "postgresql" (REQUIRED)
     type: "sqlite"  # For local development
     # For production with Docker, use:
     # type: "postgresql"
     
     # Database connection URL (REQUIRED)
     url: "sqlite:///./arxiv_db.sqlite"
     # For production with Docker, use PostgreSQL:
     # url: "postgresql://arxiv:arxiv@db:5432/arxiv_db"
   
   llm:
     provider: "local"  # or "openai"
     local:
       base_url: "http://127.0.0.1:1234"
       model: "qwen/qwen3-vl-8b"
       endpoint: "/v1/responses"
     openai:
       api_key: "your-api-key"
       model: "gpt-4"
   ```
   
   **Note:** 
   - Both `database.type` and `database.url` are **REQUIRED** in config.yaml
   - You can override `database.url` using the `DATABASE_URL` environment variable
   - The application will raise an error if database configuration is missing

5. **Set up database:**
   ```bash
   # Run migrations (creates SQLite database if using default config)
   alembic upgrade head
   ```

7. **Run the backend:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

   The API will be available at `http://localhost:8000`
   API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run development server:**
   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`
   
   **Note:** The Next.js dev server proxies `/api` requests to `http://localhost:8000` automatically.

4. **Build for production:**
   ```bash
   npm run build
   ```

5. **Start production server:**
   ```bash
   npm start
   ```

## Project Structure

```
src/web/
├── backend/                 # Python FastAPI backend
│   ├── app/
│   │   ├── domain/         # Domain layer (entities, value objects, repositories)
│   │   ├── application/    # Application layer (use cases, DTOs)
│   │   ├── infrastructure/ # Infrastructure layer (database, external clients)
│   │   └── presentation/   # Presentation layer (API routes, schemas)
│   ├── config/             # Configuration files
│   ├── alembic/            # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                # Next.js (React) frontend
│   ├── src/
│   │   ├── app/            # Next.js App Router pages
│   │   ├── api/            # API service layer
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── types/          # TypeScript types
│   ├── package.json
│   ├── next.config.ts      # Next.js configuration
│   └── tsconfig.json       # TypeScript configuration
└── docker-compose.yml      # Docker Compose configuration
```

## API Endpoints

### Papers
- `GET /api/papers` - List papers (with optional category filter, pagination)
- `GET /api/papers/{id}` - Get paper details with summary

### Categories
- `GET /api/categories` - Get all categories
- `POST /api/categories` - Update categories configuration

### Workflow
- `POST /api/workflow/trigger` - Trigger arXiv parsing workflow
  ```json
  {
    "categories": ["cs.AI", "cs.LG"],
    "num_papers": 50,
    "summarize_prompt": ""
  }
  ```

## Usage

1. **Configure Categories:**
   - Navigate to the Config page in the frontend
   - Add arXiv categories you want to monitor (e.g., `cs.AI`, `cs.LG`, `cs.CV`)

2. **Trigger Workflow:**
   - Go to the Workflow page
   - Select categories and number of papers
   - Click "Trigger Workflow"
   - The system will:
     - Fetch papers from arXiv
     - Check for duplicates (by PDF link)
     - Download and extract PDF text
     - Clean the text (remove references, etc.)
     - Generate summaries using LLM
     - Store results in database

3. **View Papers:**
   - Browse parsed papers on the Papers page
   - Click on a paper to view details and summary
   - Filter by category

## Database Schema

### Papers Table
- `id` (UUID) - Primary key
- `title` (VARCHAR) - Paper title
- `pdf_link` (VARCHAR, unique) - PDF URL
- `arxiv_id` (VARCHAR) - ArXiv ID
- `category` (VARCHAR) - Category (e.g., cs.AI)
- `summary` (JSONB) - Generated summary
- `parsed_at` (TIMESTAMP) - When paper was parsed
- `created_at` (TIMESTAMP) - When record was created

### Categories Table
- `id` (UUID) - Primary key
- `name` (VARCHAR, unique) - Category name
- `enabled` (BOOLEAN) - Whether category is enabled
- `num_papers` (INTEGER) - Number of papers in category

## Development

### Running Tests

Backend:
```bash
cd backend
pytest
```

### Database Migrations

Create a new migration:
```bash
cd backend
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

### Code Structure (DDD)

The backend follows Domain-Driven Design:

- **Domain Layer**: Contains business logic, entities, value objects, and repository interfaces
- **Application Layer**: Contains use cases and DTOs
- **Infrastructure Layer**: Contains database implementations, external API clients
- **Presentation Layer**: Contains API routes and request/response schemas

## Troubleshooting

### Backend Issues

1. **Database connection errors:**
   - Check `DATABASE_URL` in `.env` file
   - Ensure PostgreSQL is running
   - Verify database credentials

2. **LLM connection errors:**
   - Check `config/config.yaml` settings
   - Ensure LLM server is running (if using local LLM)
   - Verify API key (if using OpenAI)

3. **Migration errors:**
   - Run `alembic upgrade head` to apply migrations
   - Check database connection

### Frontend Issues

1. **API connection errors:**
   - Verify backend is running on port 8000
   - Check CORS settings in backend
   - Check browser console for errors

2. **Build errors:**
   - Run `npm install` to ensure dependencies are installed
   - Clear `node_modules` and reinstall if needed

## Environment Variables

### Backend (config/config.yaml)
All backend configuration is in `config/config.yaml`:
- Database URL
- LLM provider settings

### Frontend
The frontend uses Vite's proxy configuration (see `vite.config.ts`) to connect to the backend API.

## License

This project is provided as-is for personal and educational use.

