# HTTP API

Base URL (local): `http://localhost:5000/api`  
Interactive docs: `http://localhost:5000/docs`

Authenticated routes expect:

```
Authorization: Bearer <token>
```

Errors return `{ "error": "message" }`.

| Method | Path | Auth | Description |
| --- | --- | --- | --- |
| GET | `/health` | no | Database mode and LLM provider |
| GET | `/destinations` | no | Destination catalog |
| GET | `/templates` | no | Ready-made itinerary summaries |
| GET | `/templates/{id}` | no | Full template with days |
| POST | `/templates/{id}/clone` | yes | Save a template as a trip |
| POST | `/auth/register` | no | `{ name, email, password }` |
| POST | `/auth/login` | no | `{ email, password }` |
| GET | `/auth/me` | yes | Current user + preferences |
| GET / PUT | `/preferences` | yes | Traveler profile |
| POST | `/recommendations` | yes | Ranked destinations |
| GET / POST | `/trips` | yes | List trips / create + generate |
| GET / PUT / DELETE | `/trips/{id}` | yes | Read, rename, delete |
| POST | `/trips/{id}/generate` | yes | Rebuild the whole plan |
| POST | `/trips/{id}/refine` | yes | Feedback; optional `day_number` |
| POST | `/trips/{id}/share` | yes | Public share token + URL |
| GET | `/share/{token}` | no | Public itinerary |
| GET | `/trips/{id}/export?format=json\|md\|ics` | yes | Download |
| POST | `/trips/{id}/days/{dayId}/activities` | yes | Add a stop |
| DELETE | `/trips/{id}/activities/{activityId}` | yes | Remove a stop |

`POST /trips` body (abridged):

```json
{
  "destination": "Paris",
  "start_date": "2026-11-06",
  "end_date": "2026-11-08",
  "travelers": 1,
  "companions": "solo",
  "travel_style": "food",
  "budget": 1200,
  "interests": ["food", "museums"]
}
```
