# CrystalClear

Political transparency network analysis and visualization platform.

CrystalClear maps and analyses relationships between political agents, institutions, assets, and business participations. It provides temporal analysis tools to track how influence networks evolve over time, supporting democratic accountability and public scrutiny.

## Stack

- **Backend:** Python 3.12 + FastAPI
- **Frontend:** React 18 + TypeScript + Cytoscape.js
- **Databases:** Neo4j 5 (graph) + PostgreSQL 16 (structured data)
- **Testing:** pytest + Vitest + Playwright

## Quick Start

```bash
# Clone and start all services
git clone <repo-url>
cd crystalclear
docker compose up -d

# Backend:  http://localhost:8000/api/docs
# Frontend: http://localhost:5173
# Neo4j:    http://localhost:7474
```

## Development

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
pytest
```

### Frontend

```bash
cd frontend
npm install
npm run dev
npm test
```

## Project Structure

```
crystalclear/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/          # Route handlers
│   │   ├── core/         # Config, security, dependencies
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic DTOs
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access layer
│   │   └── graph/        # Graph engine (NetworkX)
│   └── tests/
├── frontend/             # React + TypeScript application
│   └── src/
│       ├── components/   # Reusable UI components
│       ├── pages/        # Route pages
│       ├── hooks/        # Custom React hooks
│       ├── services/     # API client
│       ├── store/        # Zustand state
│       └── types/        # TypeScript interfaces
├── knowledge-base/       # Agent knowledge base
└── docker-compose.yml
```

## Architecture

See `knowledge-base/architecture/system-overview.md` for the full architecture documentation.

## License

This project is developed as part of the Integrative Project course at the University of Porto.
