# Workout Tracker API

Flask REST API for tracking workouts and exercises with SQLite storage.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /workouts | List all workouts |
| POST | /workouts | Create a workout |
| GET | /workouts/`<id>` | Get workout details |
| PUT | /workouts/`<id>` | Update workout |
| DELETE | /workouts/`<id>` | Delete workout |
| POST | /workouts/`<id>`/exercises | Add exercise to workout |

## Examples

```bash
# Create a workout
curl -X POST http://localhost:5007/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2019-12-01", "type": "strength", "duration": 60, "notes": "Leg day"}'
# {"id": 1, "date": "2019-12-01", "type": "strength", "duration": 60}

# List workouts
curl http://localhost:5007/workouts

# Add exercise to workout
curl -X POST http://localhost:5007/workouts/1/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Squat", "sets": 4, "reps": 8, "weight": 80}'

# Get full workout with exercises
curl http://localhost:5007/workouts/1

# Delete workout
curl -X DELETE http://localhost:5007/workouts/1
```
