# Waypoint - AI Travel Itinerary Planner

Waypoint helps solo travelers, couples, and small groups build personalized day-by-day travel plans. Start with a curated itinerary or enter a destination, dates, budget, travel style, and preferences to generate a plan you can save, edit, share, and export.

[![React](https://img.shields.io/badge/frontend-React%20%2B%20Vite-61dafb?logo=react&logoColor=white)](5.%20Project%20Development%20Phase/frontend)
[![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688?logo=fastapi&logoColor=white)](5.%20Project%20Development%20Phase/backend)
[![Supabase](https://img.shields.io/badge/data-Supabase%20%2F%20SQLite-3ecf8e?logo=supabase&logoColor=white)](5.%20Project%20Development%20Phase/backend/database)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](5.%20Project%20Development%20Phase/LICENSE)

Repository: [2praveen6/travel-itinerary-skill-wallet](https://github.com/2praveen6/travel-itinerary-skill-wallet)

## Project Details

| Field | Details |
| --- | --- |
| Project | Waypoint - AI Travel Itinerary Planner |
| Developer and presenter | Praveen Singh, sole project contributor |
| Team ID | 0827CY231053 |
| Application type | React web application with a Python/FastAPI backend |
| Completed documentation | 22 project reports in the downloadable ZIP bundle |
| Last documentation update | 23 October 2026 |

Praveen Singh completed the project planning, design, frontend/backend development, AI integration, database work, testing, deployment setup, documentation, and demonstration.

## Features

- **Ready-made itineraries:** Curated trips for Paris, Bali, Goa, Kyoto, Barcelona, and Tokyo, with the option to save a dated copy.
- **Custom trip builder:** Destination, dates, budget, number of travelers, travel style, pace, interests, and dietary/mobility notes.
- **AI-assisted planning:** Structured itineraries from a configured model provider, with local rule-based generation when the selected provider is unavailable.
- **Daily timeline:** Dated days with themes, activities, dining, stays, transport suggestions, and estimated costs.
- **Authentication and preferences:** Email/password registration, JWT login, and saved traveler preferences.
- **Trip management:** Saved-trip dashboard, activity changes, regeneration, and refinement requests.
- **Sharing and export:** Public itinerary links; Markdown and ICS downloads from the interface; JSON export through the API.
- **Destination recommendations:** Destinations ranked from traveler preferences using AI or local catalog scoring.

## Project Structure

| # | Folder | Contents |
| --- | --- | --- |
| 1 | [Brainstorming & Ideation](1.%20Brainstorming%20and%20Ideation/) | Problem statements, empathy map, and initial project ideas |
| 2 | [Requirement Analysis](2.%20Requirement%20Analysis/) | Customer journey, functional/non-functional requirements, data flow, and technology stack |
| 3 | [Project Design Phase](3.%20Project%20Design%20Phase/) | Problem-solution fit, proposed solution, architecture, and database schemas |
| 4 | [Project Planning Phase](4.%20Project%20Planning%20Phase/) | Backlog, proposed sprint schedule, estimates, and project planning |
| 5 | [Project Development Phase](5.%20Project%20Development%20Phase/) | Backend/frontend source, dependency files, deployment configuration, and implementation reports |
| 6 | [Project Testing](6.%20Project%20Testing/) | Performance-testing scenarios, targets, and measurement status |
| 7 | [Project Documentation](7.%20Project%20Documentation/) | Detailed project report, executable-files guide, API, architecture, setup, and deployment guides |
| 8 | [Project Demonstration](8.%20Project%20Demonstration/) | Demo planning, proposed features, communication, future plan, sole-member involvement, and application preview |
| - | [Output](output/) | Complete PDF bundle and standalone involvement report |

The application source is inside **5. Project Development Phase/backend** and **5. Project Development Phase/frontend**. Use these paths when running the project or configuring hosting.

## Completed PDF Reports

**[Download all 22 completed project PDFs](output/Waypoint%20-%20Completed%20Project%20Templates.zip)**

The reports were completed using the supplied PDF templates and Waypoint project information. They include Team ID **0827CY231053**. General reports omit member names and assignment fields; the involvement report identifies **Praveen Singh as the sole developer and presenter**.

| Phase | Reports included in the bundle | Count |
| --- | --- | --- |
| Brainstorming & Ideation | Brainstorming & Idea Prioritization; Define Problem Statements; Empathy Map | 3 |
| Requirement Analysis | Customer Journey Map; Solution Requirements; Data Flow Diagram; Technology Stack | 4 |
| Project Design | Problem-Solution Fit; Proposed Solution; Solution Architecture | 3 |
| Project Planning | Project Planning | 1 |
| Project Development | Coding & Solution; Code-Layout, Readability and Reusability; No. of Functional Features Included in the Solution | 3 |
| Project Testing | Performance Testing | 1 |
| Project Documentation | Project Executable Files; Sample Project Documentation | 2 |
| Project Demonstration | Project Demo Planning; Demonstration of Proposed Features; Communication; Scalability & Future Plan; Team Involvement in Demonstration | 5 |
| **Total** | | **22** |

Selected completed reports:

- [Brainstorming & Idea Prioritization](1.%20Brainstorming%20and%20Ideation/Brainstorming%20%26%20Idea%20Prioritization%20-%20Waypoint.pdf)
- [Team Involvement in Demonstration](output/pdf/Team%20Involvement%20in%20Demonstration%20-%20Waypoint.pdf)

The latest involvement report includes possible demo issues such as slow AI responses or temporary backend connection errors, with fixes to retry generation, use the rule-based planner, or restart the backend. These are example issues and remedies.

## Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | JavaScript/JSX, React 18, Vite 5, React Router 6, CSS |
| UI tools | Framer Motion, Lucide React |
| Backend | Python 3.11+, FastAPI, Pydantic, Uvicorn; Gunicorn for hosted serving |
| Authentication | bcrypt password hashing and signed JWTs through python-jose |
| Storage | Supabase Postgres when configured; SQLite for local operation |
| AI integrations | Groq, OpenAI, Hugging Face, and explicitly selected Ollama |
| Deployment configuration | Render for the API, Vercel for the frontend, Supabase for hosted storage |

### AI and Database Behavior

With `LLM_PROVIDER=auto`, the backend chooses Groq when its key is configured, otherwise OpenAI, otherwise Hugging Face. Set `LLM_PROVIDER=ollama` to select a local Ollama model explicitly.

If the selected provider fails or no provider is configured, the itinerary engine generates a plan using local rules. The current implementation selects one provider per request; it does not retry every other provider after a failed call.

Supabase mode is enabled when `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY` are configured. Otherwise the backend uses SQLite. These are alternative storage modes; SQLite does not mirror a live Supabase database.

## Quick Start

Prerequisites: **Python 3.11 or newer**, **Node.js 18 or newer**, and a browser. The commands below use Windows PowerShell and start from the repository root.

### 1. Backend

```powershell
cd "5. Project Development Phase/backend"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit the new `.env` file and set a strong `SECRET_KEY` or `JWT_SECRET`. Keep the local frontend origin as `http://localhost:5173`. Leave optional AI and Supabase credentials empty to run with SQLite and rule-based planning.

Start the API:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 5000
```

- Health check: <http://localhost:5000/api/health>
- Interactive API documentation: <http://localhost:5000/docs>

### 2. Frontend

Open a second PowerShell terminal at the repository root:

```powershell
cd "5. Project Development Phase/frontend"
npm install
npm run dev
```

Open **<http://localhost:5173>**. For local development, leave `VITE_API_URL` empty to use Vite's `/api` proxy to port 5000.

To build the frontend:

```powershell
npm run build
```

### 3. Try the Main Workflow

1. Register and log in.
2. Browse **Explore** and save a curated itinerary, or use **Custom** to generate a trip.
3. Open **My trips**, review the daily timeline, and edit activities as needed.
4. Try a refinement request and review the returned days.
5. Create a public share link and export Markdown or an ICS calendar file.
6. Open **Ideas** to view destination recommendations.

### Optional Service Settings

| Service | Environment settings |
| --- | --- |
| Groq | `GROQ_API_KEY`, optional `GROQ_MODEL` |
| OpenAI | `OPENAI_API_KEY`, optional `OPENAI_MODEL` |
| Hugging Face | `HF_TOKEN`, optional `HF_MODEL` |
| Ollama | `LLM_PROVIDER=ollama`, `OLLAMA_URL`, `OLLAMA_MODEL` |
| Supabase | `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`; initialize tables with `backend/database/schema.sql` |

Keep provider credentials and database service keys in the backend environment. The frontend only needs `VITE_API_URL` when connecting to a hosted API.

## Testing and Current Limitations

The [detailed project report](7.%20Project%20Documentation/Sample%20Project%20Documentation%20-%20Waypoint.pdf) notes 10 manual functional test cases previously reported as passed. The [performance-testing report](6.%20Project%20Testing/Performance%20Testing%20-%20Waypoint.pdf) contains proposed scenarios and targets; actual load-test measurements remain marked **Not measured / Not run**. This README update did not rerun the application tests.

- Review activity suggestions, costs, transfer times, and availability before travel; these are planning estimates.
- Per-day refinement requests are supported, but the current endpoint replaces the returned plan. Preserving all other days needs validation, especially with the rule-based engine.
- Public deployment URLs and a demo-video link are not recorded in the project documentation.
- Capacity, latency, and uptime targets require measured evidence before being presented as achieved results.

## Deployment

| Service | Project directory | Configuration |
| --- | --- | --- |
| Render API | `5. Project Development Phase/backend` | Install `requirements.txt`; run Gunicorn with a Uvicorn worker; set backend secrets and frontend origin |
| Vercel frontend | `5. Project Development Phase/frontend` | Run `npm run build`, publish `dist`, and set `VITE_API_URL` to the hosted API origin |
| Supabase database | `5. Project Development Phase/backend/database` | Apply `schema.sql` and the trips migration when upgrading an existing database |

The supplied [Render blueprint](5.%20Project%20Development%20Phase/render.yaml) still lists `rootDir: backend`. Adjust that setting to the nested backend path when using the blueprint from the repository root.

After deployment, update `FRONTEND_URL` / `CLIENT_ORIGIN`, verify `/api/health`, and check that public share links use the hosted frontend origin. See the [deployment guide](7.%20Project%20Documentation/DEPLOYMENT.md) for service configuration details.

## Project Guides and Demonstration

- [Local setup](7.%20Project%20Documentation/SETUP.md)
- [API reference](7.%20Project%20Documentation/API.md)
- [Architecture](7.%20Project%20Documentation/ARCHITECTURE.md)
- [Deployment](7.%20Project%20Documentation/DEPLOYMENT.md)
- [Contribution guide](7.%20Project%20Documentation/CONTRIBUTING.md)
- [Demonstration plan](8.%20Project%20Demonstration/Project%20Demo%20Planning%20-%20Waypoint.pdf)

Some guides retain older root-level `backend` / `frontend` examples. Use the current phase-folder paths shown in this README.

![Waypoint application preview](8.%20Project%20Demonstration/preview.png)

## Future Scope

- Multi-city trip planning.
- Collaborative trip editing.
- Offline access to saved itineraries.
- Native mobile application.
- More reliable unchanged-day refinement, broader destination coverage, and measured performance improvements.

## License

MIT - see [LICENSE](5.%20Project%20Development%20Phase/LICENSE).
