# Expense API

Flask REST API for personal expense tracking with category filtering and monthly reports.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | /expenses | List expenses (filter: category, start, end) |
| POST | /expenses | Add expense |
| GET | /expenses/`<id>` | Get expense |
| PUT | /expenses/`<id>` | Update expense |
| DELETE | /expenses/`<id>` | Delete expense |
| GET | /expenses/summary | Monthly summary |

## Examples

```bash
# Add expense
curl -X POST http://localhost:5003/expenses \
  -H "Content-Type: application/json" \
  -d '{"amount": 12.50, "description": "Lunch", "category": "food"}'

# List all expenses
curl http://localhost:5003/expenses

# Filter by category
curl "http://localhost:5003/expenses?category=food"

# Filter by date range
curl "http://localhost:5003/expenses?start=2019-10-01&end=2019-10-31"

# Monthly summary
curl "http://localhost:5003/expenses/summary?month=2019-10"
# {"month": "2019-10", "total": 450.75, "by_category": {"food": 120.50, "transport": 80.25}}

# Delete expense
curl -X DELETE http://localhost:5003/expenses/1
```
