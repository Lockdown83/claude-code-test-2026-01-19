# VC Job Scraper

A web-based application for scraping and tracking VC job opportunities across multiple sources.

## Features

- Automated job scraping from multiple sources (LinkedIn, AngelList, VC firm career pages, Indeed, Glassdoor)
- Duplicate detection using fuzzy matching
- Application tracking (saved → applied → interviewing → offer)
- Browser-based UI for managing jobs and applications

## Tech Stack

**Backend:**
- FastAPI (async Python web framework)
- SQLite database with SQLAlchemy ORM
- Playwright (browser automation)
- BeautifulSoup4 (HTML parsing)
- RapidFuzz (fuzzy string matching)
- Celery + Redis (background tasks)

**Frontend:**
- React with Vite
- Axios for API calls

## Project Structure

```
sandbox/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI app entry point
│   │   ├── config.py    # Configuration settings
│   │   ├── database.py  # Database connection
│   │   ├── models/      # SQLAlchemy models
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── scrapers/    # Job scrapers
│   │   ├── services/    # Business logic
│   │   └── api/         # API routes
│   ├── alembic/         # Database migrations
│   └── requirements.txt
│
└── frontend/            # React frontend
    ├── src/
    │   ├── App.jsx      # Main app component
    │   ├── components/  # React components
    │   └── services/    # API client
    └── package.json
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure:
```bash
cp .env.example .env
# Edit .env with your settings
```

5. Initialize the database:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

6. Install Playwright browsers (for web scraping):
```bash
playwright install
```

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Copy the example environment file:
```bash
cp .env.example .env
```

## Running the Application

### Start the Backend

From the `backend` directory:

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the FastAPI server
uvicorn app.main:app --reload
```

The API will be available at: http://localhost:8000
API documentation: http://localhost:8000/docs

### Start Celery Worker (Optional - for background tasks)

In a separate terminal, from the `backend` directory:

```bash
# Make sure Redis is running first
redis-server

# In another terminal, start Celery worker
celery -A app.tasks.celery_app worker --loglevel=info
```

### Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

The frontend will be available at: http://localhost:5173

## Development Status

### ✅ Phase 1: Foundation (COMPLETED)
- [x] Project structure setup
- [x] FastAPI backend initialized
- [x] React frontend initialized
- [x] Database models created
- [x] Alembic migrations configured

### 🚧 Phase 2: Core Backend (IN PROGRESS)
- [ ] CRUD operations for jobs
- [ ] CRUD operations for applications
- [ ] Deduplication service
- [ ] Pydantic schemas

### 📋 Phase 3: Scraping (TODO)
- [ ] Base scraper class
- [ ] Indeed scraper
- [ ] VC firm scraper
- [ ] LinkedIn scraper
- [ ] AngelList scraper

### 📋 Phase 4: Frontend (TODO)
- [ ] Job list component
- [ ] Job card component
- [ ] Application tracker
- [ ] Scraping controls

### 📋 Phase 5: Integration & Testing (TODO)
- [ ] End-to-end testing
- [ ] UI/UX polish

### 📋 Phase 6: Deployment (TODO)
- [ ] Docker setup
- [ ] Documentation

## API Endpoints

### Jobs
- `GET /api/jobs` - List jobs
- `GET /api/jobs/{id}` - Get job details
- `POST /api/jobs` - Create job
- `DELETE /api/jobs/{id}` - Delete job

### Applications
- `GET /api/applications` - List applications
- `POST /api/applications` - Create application
- `PUT /api/applications/{id}` - Update application

### Scraping
- `POST /api/scraping/start` - Start scraping
- `GET /api/scraping/status` - Check status
- `GET /api/scraping/logs` - View logs

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Important Notes

### Legal Considerations
⚠️ **LinkedIn explicitly prohibits automated scraping** - consider using their official API or manual job entry as an alternative.

- Respect robots.txt on all sites
- Add delays between requests (2-5 seconds)
- Only scrape publicly available data
- Comply with each site's Terms of Service

### Development Tips

1. Start with easier sources (Indeed, VC firm career pages)
2. Check for official APIs before implementing scrapers
3. Implement robust error handling
4. Monitor scraping success rates
5. Consider using job board APIs as alternatives

## License

This is a personal project for educational and job search purposes.

## Contributing

This is a personal sandbox project. Feel free to fork and modify for your own use.
