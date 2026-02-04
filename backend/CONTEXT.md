# VC Dashboard - Complete System Context

**Version:** 1.0.0
**Last Updated:** 2026-02-04

---

## 🎯 Project Overview

**VC Dashboard** is a gamified tracking system for breaking into Venture Capital. It combines job application tracking with dealflow sourcing, featuring streaks, goals, conversion metrics, and visual feedback to motivate consistent activity.

**Three Access Methods:**
1. **Web Frontend** - Next.js dashboard at http://localhost:3000
2. **REST API** - FastAPI backend at http://localhost:8000
3. **CLI Tool** - Terminal interface via `vc-dashboard` command

---

## 📁 Project Structure

```
backend/
├── app/
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration (DB, Exa API)
│   ├── database.py                # SQLAlchemy async setup
│   ├── models/                    # SQLAlchemy models
│   │   ├── job.py                 # Job postings
│   │   ├── application.py         # Job applications
│   │   ├── startup.py             # Startup companies
│   │   ├── dealflow.py            # Dealflow tracking
│   │   ├── goal.py                # Weekly goals
│   │   └── activity.py            # Activity log for streaks
│   ├── schemas/                   # Pydantic schemas
│   │   ├── job.py
│   │   ├── application.py
│   │   └── ...
│   ├── api/routes/                # API route handlers
│   │   ├── dashboard.py           # Dashboard stats endpoint
│   │   ├── jobs.py                # Jobs CRUD
│   │   ├── applications.py        # Applications CRUD
│   │   ├── startups.py            # Startups CRUD
│   │   ├── dealflow.py            # Dealflow CRUD
│   │   ├── goals.py               # Goals management
│   │   └── scraping.py            # Exa API scraping
│   └── services/                  # Business logic
│       ├── job_service.py
│       ├── application_service.py
│       ├── exa_service.py         # Exa API integration
│       ├── dashboard_service.py   # Gamification calculations
│       ├── deduplication.py       # Duplicate detection
│       └── scraping.py            # Job/startup scraping
├── cli.py                         # CLI main entry point
├── cli_api.py                     # CLI API client wrapper
├── cli_config.py                  # CLI configuration
├── cli_formatters.py              # Rich formatting utilities
├── setup.py                       # CLI package setup
├── frontend/                      # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Dashboard page
│   │   └── globals.css            # Tailwind + gamification styles
│   ├── components/
│   │   ├── gamification/          # Gamification UI components
│   │   ├── layout/                # Sidebar, Header, ThemeToggle
│   │   └── ui/                    # shadcn/ui components
│   ├── lib/
│   │   ├── api.ts                 # Axios API client
│   │   └── types.ts               # TypeScript types
│   ├── hooks/
│   │   └── useApi.ts              # SWR data fetching hooks
│   └── .env.local                 # Frontend environment
├── .env                           # Backend environment
├── requirements.txt               # Python dependencies
├── vc_dashboard.db                # SQLite database
├── CONTEXT.md                     # This file
├── FRONTEND_SUMMARY.md            # Frontend documentation
└── IMPLEMENTATION_SUMMARY.md      # Backend documentation
```

---

## 🚀 Quick Start Commands

### Initial Setup

```bash
# 1. Create and activate virtual environment
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# OR: venv\Scripts\activate  # Windows

# 2. Install backend dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Edit .env and add your EXA_API_KEY

# 4. Initialize database
alembic upgrade head

# 5. Install CLI tool
pip install -e .

# 6. Install frontend dependencies
cd frontend
npm install
```

### Running the System

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
# Running at: http://localhost:8000
```

**Terminal 2 - Frontend:**
```bash
cd backend/frontend
npm run dev
# Running at: http://localhost:3000
```

**Terminal 3 - CLI:**
```bash
cd backend
source venv/bin/activate
vc-dashboard dashboard summary
```

---

## 🎮 CLI Commands Reference

### Dashboard Commands
```bash
vc-dashboard dashboard summary          # Quick overview
vc-dashboard dashboard stats            # Detailed statistics
vc-dashboard dashboard streak           # View current streaks
```

### Job Commands
```bash
vc-dashboard jobs list                  # List all jobs
vc-dashboard jobs search "VC Analyst"   # Search jobs by title
vc-dashboard jobs view 1                # View job details
vc-dashboard jobs scrape "VC jobs" 50   # Scrape jobs via Exa API
```

### Application Commands
```bash
vc-dashboard apps list                  # List all applications
vc-dashboard apps list --status applied # Filter by status
vc-dashboard apps create 1              # Create application for job ID 1
vc-dashboard apps view 1                # View application details
vc-dashboard apps update 1 --status interviewing
vc-dashboard apps delete 1              # Delete application
```

### Startup Commands
```bash
vc-dashboard startups list              # List all startups
vc-dashboard startups search "AI"       # Search startups
vc-dashboard startups view 1            # View startup details
vc-dashboard startups scrape --accelerator "YC" --batch "W24" --num-results 30
```

### Dealflow Commands
```bash
vc-dashboard dealflow list              # List all dealflow items
vc-dashboard dealflow list --status contacted
vc-dashboard dealflow view 1            # View dealflow details
vc-dashboard dealflow create 1          # Create dealflow for startup ID 1
vc-dashboard dealflow update 1 --status meeting
vc-dashboard dealflow contact 1 email   # Log email contact
vc-dashboard dealflow contact 1 meeting # Log meeting
vc-dashboard dealflow delete 1
```

### Scraping Commands
```bash
# Job scraping
vc-dashboard scrape jobs "VC Analyst positions" 50
vc-dashboard scrape firms "Sequoia,a16z,Benchmark" 10

# Startup scraping
vc-dashboard scrape accelerator "YC" "W24" 30
vc-dashboard scrape sectors "AI,Climate,Fintech" 20
```

### Goal Commands
```bash
vc-dashboard goals view                 # View current goals
vc-dashboard goals set --jobs 15 --startups 8
vc-dashboard goals reset                # Reset to defaults
```

### Configuration
```bash
vc-dashboard config show                # Show current config
vc-dashboard config set api_url "http://localhost:8000"
```

---

## 🌐 API Endpoints Reference

### Base URL
```
http://localhost:8000
```

### Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Dashboard
```
GET  /api/dashboard/stats              # Get all gamification stats
```

### Jobs
```
GET    /api/jobs/                      # List jobs (supports filters)
GET    /api/jobs/{id}                  # Get job by ID
POST   /api/jobs/                      # Create job
PUT    /api/jobs/{id}                  # Update job
DELETE /api/jobs/{id}                  # Delete job
GET    /api/jobs/stats                 # Job statistics
```

### Applications
```
GET    /api/applications/              # List applications
GET    /api/applications/{id}          # Get application by ID
POST   /api/applications/              # Create application
PUT    /api/applications/{id}          # Update application
DELETE /api/applications/{id}          # Delete application
GET    /api/applications/stats         # Application statistics
```

### Startups
```
GET    /api/startups/                  # List startups
GET    /api/startups/{id}              # Get startup by ID
POST   /api/startups/                  # Create startup
PUT    /api/startups/{id}              # Update startup
DELETE /api/startups/{id}              # Delete startup
```

### Dealflow
```
GET    /api/dealflow/                  # List dealflow items
GET    /api/dealflow/{id}              # Get dealflow by ID
POST   /api/dealflow/                  # Create dealflow
PUT    /api/dealflow/{id}              # Update dealflow
DELETE /api/dealflow/{id}              # Delete dealflow
POST   /api/dealflow/{id}/contact      # Log contact (email/meeting)
GET    /api/dealflow/stats             # Dealflow statistics
```

### Goals
```
GET    /api/goals/current              # Get current weekly goals
POST   /api/goals/                     # Create/update goals
PUT    /api/goals/{id}                 # Update goal
```

### Scraping
```
POST   /api/scraping/start             # Scrape jobs via Exa
POST   /api/scraping/search-firms      # Search specific VC firms
POST   /api/dealflow-scraping/accelerator  # Scrape accelerator batch
POST   /api/dealflow-scraping/sectors      # Scrape by sectors
```

---

## 🎨 Data Models & Schema

### Job
```typescript
{
  id: number;
  title: string;
  company: string;
  location: string;
  job_type: string;           // "full-time", "part-time", "contract"
  seniority_level: string;    // "entry", "mid", "senior", "director"
  description: string;
  salary_range: string;
  source: string;             // "manual", "exa", "linkedin"
  source_url: string;
  posted_date: string;        // ISO datetime
  scraped_at: string;         // ISO datetime
  is_active: boolean;
  tags: string;               // Comma-separated
}
```

### Application
```typescript
{
  id: number;
  job_id: number;
  status: "saved" | "applied" | "interviewing" | "rejected" | "offer" | "accepted";
  applied_date: string;
  notes: string;
  resume_version: string;
  cover_letter_path: string;
  last_contact_date: string;
  next_follow_up_date: string;
  interview_count: number;
  interview_notes: string;
  created_at: string;
  updated_at: string;
}
```

### Startup
```typescript
{
  id: number;
  name: string;
  website: string;
  description: string;
  funding_stage: string;      // "pre-seed", "seed", "Series A", etc.
  last_funding_date: string;
  funding_amount: string;
  valuation: string;
  traction_metrics: string;
  founders: string;
  industry: string;
  tags: string;
  source: string;
  source_url: string;
  discovered_date: string;
  last_updated: string;
  is_active: boolean;
}
```

### Dealflow
```typescript
{
  id: number;
  startup_id: number;
  status: "sourced" | "researching" | "contacted" | "meeting" | "shared" | "progressing" | "closed";
  first_contact_date: string;
  last_contact_date: string;
  emails_sent: number;
  meetings_held: number;
  notes: string;
  research_summary: string;
  outcome: string;            // "passed", "invested", "introduced", "watching"
  outcome_reason: string;
  intro_made_to: string;      // Name of person introduced to
  intro_date: string;
  created_at: string;
  updated_at: string;
}
```

### Dashboard Stats Response
```typescript
{
  jobs: {
    total_active: number;
    applications: {
      total: number;
      by_status: { [status: string]: number };
      response_rate: number;      // 0.0 to 1.0
      interview_rate: number;
      offer_rate: number;
    };
    activity_last_7_days: number;
    weekly_goal: {
      target: number;
      current: number;
      progress: number;           // 0.0 to 1.0
    };
    current_streak: number;
  };
  dealflow: {
    total_startups: number;
    pipeline: { [status: string]: number };
    conversion_rates: {
      sourced_to_contacted: number;
      contacted_to_meeting: number;
      meeting_to_shared: number;
    };
    network_growth: {
      total_emails_sent: number;
      total_meetings_held: number;
      intros_made: number;
    };
    activity_last_7_days: {
      new_startups: number;
      emails_sent: number;
      meetings_held: number;
    };
    weekly_goal: {
      target: number;
      current: number;
      progress: number;
    };
    current_streak: number;
  };
  combined: {
    total_activity_last_7_days: number;
    overall_streak: number;
  };
}
```

---

## 🎯 Gamification System

### Streak Tracking
- **How it works:** Tracks consecutive days with activity (applications or dealflow actions)
- **Calculation:** Last activity date compared to today
- **Reset:** If no activity for a day, streak resets to 0
- **Types:** Jobs streak, Dealflow streak, Overall streak (combined)

**Streak Tiers:**
- 0 days: Gray (inactive)
- 1-6 days: Orange (warming up)
- 7-29 days: Yellow (on fire)
- 30+ days: Red (legendary)

### Weekly Goals
- **Default Targets:** 10 job applications, 5 startups per week
- **Week Start:** Monday
- **Reset:** Automatically resets every Monday
- **Progress:** Calculated as current/target (0.0 to 1.0)
- **Customizable:** Can be changed via CLI or API

### Conversion Metrics
**Response Rate:**
```
interviews_received / total_applications
```

**Interview Rate:**
```
applications_with_interview / total_applications
```

**Offer Rate:**
```
offers_received / total_applications
```

**Color Coding:**
- Green (≥30%): Excellent
- Yellow (15-30%): Good
- Red (<15%): Needs improvement

### Network Growth
- **Emails Sent:** Total emails logged in dealflow
- **Meetings Held:** Total meetings logged in dealflow
- **Intros Made:** Total introductions to VCs/partners

---

## 🔧 Configuration

### Environment Variables

**Backend (.env):**
```env
# Required
EXA_API_KEY=your_exa_api_key_here

# Optional
DATABASE_URL=sqlite+aiosqlite:///./vc_dashboard.db
```

**Frontend (.env.local):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Getting Exa API Key
1. Sign up at https://exa.ai
2. Get API key from dashboard
3. Add to backend/.env

---

## 💾 Database

### Type
SQLite (async via aiosqlite)

### Location
```
backend/vc_dashboard.db
```

### Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Tables
- `jobs` - Job postings
- `applications` - Job applications
- `startups` - Startup companies
- `dealflow_applications` - Dealflow tracking
- `weekly_goals` - Weekly targets
- `activities` - Activity log for streak tracking

---

## 🎨 Frontend Architecture

### Tech Stack
- **Framework:** Next.js 16 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS v4
- **Components:** shadcn/ui (Radix UI)
- **Data Fetching:** SWR (auto-refresh every 30 seconds)
- **HTTP Client:** axios
- **Icons:** Lucide React
- **Theme:** next-themes (dark/light mode)

### Key Components

**Gamification:**
- `StreakBadge` - Flame streak indicator
- `ProgressRing` - Circular progress with SVG
- `GoalCard` - Weekly goal cards
- `ConversionMetrics` - Funnel visualization

**Layout:**
- `Sidebar` - Navigation menu
- `Header` - Top bar with theme toggle
- `ThemeToggle` - Dark/light mode switcher

### Data Flow
```
Component → useDashboard() → SWR → axios → Backend API → Database
                ↓
          Auto-refresh every 30s
                ↓
          Component re-renders
```

### NPM Commands
```bash
npm run dev         # Development server
npm run build       # Production build
npm run start       # Production server
npm run lint        # Run ESLint
```

---

## 🔌 Integration Points

### Exa API
- **Purpose:** AI-powered job and startup search
- **Endpoints Used:**
  - `search` - Semantic search for jobs/startups
  - `contents` - Get full content from URLs
- **Rate Limits:** Check Exa dashboard
- **Cost:** Pay per search request

### CLI ↔ Backend
- CLI uses `requests` library
- Calls same REST API as frontend
- Base URL configurable via `vc-dashboard config`

### Frontend ↔ Backend
- Frontend uses `axios` with baseURL from `.env.local`
- CORS enabled in FastAPI for `http://localhost:3000`
- SWR handles caching and revalidation

---

## 🚨 Common Issues & Solutions

### Port Already in Use
```bash
# Kill process on port 8000 (backend)
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000 (frontend)
lsof -ti:3000 | xargs kill -9
```

### CLI Command Not Found
```bash
# Always activate venv first
source venv/bin/activate

# Or run directly
./venv/bin/vc-dashboard dashboard summary
```

### Database Locked
```bash
# Stop all running instances
# Delete vc_dashboard.db
# Run migrations again
alembic upgrade head
```

### Frontend Can't Connect to Backend
1. Verify backend is running: `curl http://localhost:8000/api/dashboard/stats`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Restart frontend: `npm run dev`

### Exa API Errors
1. Check API key is correct in `.env`
2. Verify account has credits
3. Check rate limits

---

## 🧪 Testing

### Manual Testing
```bash
# Test backend API
curl http://localhost:8000/api/dashboard/stats

# Test CLI
vc-dashboard dashboard summary

# Test frontend
open http://localhost:3000
```

### Adding Test Data
```bash
# Via CLI
vc-dashboard jobs scrape "VC Analyst" 10
vc-dashboard apps create 1
vc-dashboard startups scrape --accelerator "YC" --batch "W24" --num-results 5
vc-dashboard dealflow create 1
```

---

## 📈 Development Workflow

### Adding a New Feature

**1. Backend:**
```bash
# Add model to app/models/
# Add schema to app/schemas/
# Add service to app/services/
# Add route to app/api/routes/
# Create migration: alembic revision --autogenerate -m "feature"
# Apply migration: alembic upgrade head
```

**2. CLI:**
```bash
# Add command to cli.py
# Add API method to cli_api.py
# Add formatter to cli_formatters.py
```

**3. Frontend:**
```bash
# Add TypeScript types to lib/types.ts
# Add API method to lib/api.ts
# Add SWR hook to hooks/useApi.ts
# Create component in components/
# Update page in app/
```

### Git Workflow
```bash
git status
git add .
git commit -m "description"
git push origin main
```

---

## 📚 Key Concepts

### Async Everything
- Backend uses `async/await` throughout
- Database queries are async (aiosqlite)
- FastAPI routes are async
- Services are async

### Type Safety
- Backend: Pydantic schemas validate all data
- Frontend: TypeScript interfaces match backend schemas
- CLI: Type hints in Python

### Separation of Concerns
- **Models:** Database structure
- **Schemas:** API request/response validation
- **Services:** Business logic
- **Routes:** HTTP endpoints
- **CLI:** User interface

### Gamification First
- Every action contributes to streaks or goals
- Dashboard shows progress visually
- Positive reinforcement for consistent activity

---

## 🎯 Design Principles

1. **Gamification at the Core** - Motivate consistent activity
2. **Three-Way Access** - Web, API, CLI for different use cases
3. **Type Safety** - TypeScript + Pydantic = no runtime surprises
4. **Async by Default** - Fast, scalable, modern
5. **Beautiful UX** - Dark mode, smooth animations, visual feedback
6. **Developer Friendly** - Clear structure, good documentation

---

## 🔮 Future Enhancements

**Phase 1 - Additional Pages:**
- Jobs list page with search/filter
- Applications kanban board
- Startups discovery page
- Dealflow pipeline view
- Settings page for customization

**Phase 2 - Advanced Features:**
- Charts and graphs (Recharts)
- Achievement badges system
- Email integration
- Calendar integration
- Export to CSV/PDF
- Mobile responsiveness

**Phase 3 - Collaboration:**
- Multi-user support
- Team leaderboards
- Shared dealflow
- Comments and notes
- Activity feed

---

## 📞 Support & Resources

**Documentation Files:**
- `CONTEXT.md` - This file (complete reference)
- `FRONTEND_SUMMARY.md` - Frontend implementation details
- `IMPLEMENTATION_SUMMARY.md` - Backend API documentation

**API Documentation:**
- Swagger: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**External Resources:**
- Next.js Docs: https://nextjs.org/docs
- FastAPI Docs: https://fastapi.tiangolo.com
- Exa API: https://docs.exa.ai

---

## 🏁 Quick Reference Card

**Start System:**
```bash
# Terminal 1
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2
cd backend/frontend && npm run dev

# Terminal 3
cd backend && source venv/bin/activate && vc-dashboard dashboard summary
```

**Access Points:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Common Commands:**
```bash
vc-dashboard dashboard stats
vc-dashboard jobs scrape "VC Analyst" 20
vc-dashboard apps create 1
vc-dashboard dealflow contact 1 email
```

**Key Files:**
- Backend config: `backend/.env`
- Frontend config: `backend/frontend/.env.local`
- Database: `backend/vc_dashboard.db`
- CLI entry: `backend/cli.py`
- Frontend entry: `backend/frontend/app/page.tsx`

---

**Version:** 1.0.0
**Last Updated:** 2026-02-04
**Maintained By:** AI-assisted development
