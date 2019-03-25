def top_urls(rows, limit=10):
    sorted_rows = sorted(rows, key=lambda x: x['clicks'], reverse=True)
    return sorted_rows[:limit]


def total_clicks(rows):
    return sum(r['clicks'] for r in rows)
