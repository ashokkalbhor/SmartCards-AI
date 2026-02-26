# Copilot Instructions for SmartCards AI

## 🏗️ Big Picture Architecture
- **Backend**: Python FastAPI app (`backend/app/`) with modular structure: `api/` (routes), `core/` (config), `models/` (DB), `schemas/` (validation), `services/` (business logic).
- **Frontend**: React 18 + TypeScript app (`frontend/src/`) using Tailwind CSS, Framer Motion, React Query. Key folders: `components/`, `pages/`, `hooks/`, `utils/`.
- **Mobile**: React Native app (`mobile/src/`) with Expo, navigation, and reusable components.
- **Database**: PostgreSQL (prod), SQLite (tests/dev), managed via SQLAlchemy ORM. Redis for caching/session.
- **Infrastructure**: Docker for local/dev, Nginx for proxy, CI/CD for deploy.

## ⚡ Developer Workflows
- **Backend**: Activate venv, install deps, run with `uvicorn app.main:app --reload`.
- **Frontend**: `npm install` then `npm run dev`.
- **Mobile**: `npm install` then `npx expo start`.
- **Testing (Backend)**:
  - Quick: `python run_tests.py`
  - Manual: `pytest --cov=app --cov-report=html --cov-fail-under=90 -v`
  - Coverage: See `htmlcov/index.html` and `coverage.xml`.
  - Isolated SQLite DB, fixtures in `conftest.py`.
- **Testing (Frontend)**: No explicit instructions found; follow React/TypeScript conventions.
- **Build/Deploy**: Use Dockerfiles and `docker-compose.yml` for local/dev. CI/CD runs tests and coverage checks.

## 🧩 Project-Specific Patterns
- **Backend**:
  - API endpoints in `app/api/`, business logic in `app/services/`.
  - Pydantic schemas for validation (`app/schemas/`).
  - JWT for auth, bcrypt for passwords, CORS/rate limiting enabled.
  - **GenAI-Powered Automation**: gpt-5 model for intelligent card data extraction and updates.
  - **Automated Card Updates**: Monthly scheduled updates via APScheduler (1st of month, midnight).
  - **Edit Suggestion System**: All automated changes go through approval workflow before applying.
  - **Community Integration**: Approved changes automatically posted to community for transparency.
  - Test suite covers API, models, core logic, admin, edit suggestions, automation services. Use markers for unit/integration/slow tests.
- **Frontend**:
  - Use React Query for data fetching/state.
  - Tailwind for styling, Framer Motion for animation.
  - Components/pages/hooks/utils separation.
- **Mobile**:
  - Expo for dev, React Native Paper for UI.
  - Offline support, push notifications, biometric auth.

## 🔗 Integration Points
- **Backend ↔ Frontend/Mobile**: REST API (FastAPI), JWT auth, CORS enabled.
- **Database**: SQLAlchemy models, migrations via Alembic (`alembic/`).
- **External**: AWS/GCP for hosting, Discord/email for support.

## 📚 Key Files & Directories
- `backend/app/api/` – API routes
  - `card_updates.py` – Manual trigger endpoints for automated updates (admin only)
- `backend/app/services/` – Business logic
  - `card_update_service.py` – GenAI extraction, comparison, edit suggestion creation
  - `web_scraping_service.py` – Fetch and clean content from bank websites
  - `card_update_scheduler.py` – APScheduler for monthly automated runs
- `backend/app/models/` – DB models
  - `edit_suggestion.py` – Approval workflow for all changes
  - `community_post.py` – Auto-generated posts for approved updates
- `backend/app/schemas/` – Pydantic schemas
- `backend/app/core/config.py` – Central config, OpenAI model setting (gpt-5)
- `backend/tests/` – Test suite, fixtures in `conftest.py`
  - `test_card_update_service.py` – Tests for extraction, comparison, suggestions
  - `test_web_scraping_service.py` – Tests for web scraping, URL validation
- `frontend/src/` – React app source
- `mobile/src/` – Mobile app source
- `docker-compose.yml`, `Dockerfile*` – Infra setup
- `README.md` – Architecture, setup, quickstart

## 📝 Example Patterns
- Backend API route:
  ```python
  @router.get("/cards/{id}")
  def get_card(id: int, db: Session = Depends(get_db)):
      ...
  ```
- Frontend data fetch:
  ```ts
  const { data } = useQuery(['cards'], fetchCards)
  ```
- Test with fixture:
  ```python
  def test_register_success(test_client, test_user):
      ...
  ```

---

**Update this file if major workflows, conventions, or architecture change.**
