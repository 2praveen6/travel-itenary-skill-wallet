# API

Base: `http://localhost:5000/api`  
Auth: `Authorization: Bearer <token>`

| Method | Path | Notes |
| --- | --- | --- |
| GET | `/health` | DB mode |
| GET | `/destinations` | Catalog |
| POST | `/auth/register` | `{ name, email, password }` |
| POST | `/auth/login` | `{ email, password }` |
| GET | `/auth/me` | User + preferences |
| GET/PUT | `/preferences` | Traveler profile |
| POST | `/recommendations` | Ranked destinations |
| GET/POST | `/trips` | List / create + generate |
| GET/PUT/DELETE | `/trips/:id` | Manage |
| POST | `/trips/:id/regenerate` | Rebuild days |
| GET | `/trips/:id/export?format=json\|md\|ics` | Export |
| POST | `/trips/:id/days/:dayId/activities` | Add stop |
| DELETE | `/trips/:id/activities/:activityId` | Remove stop |
