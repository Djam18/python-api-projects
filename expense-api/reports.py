def monthly_summary(expenses):
    summary = {}
    for e in expenses:
        month = e['date'][:7] if e['date'] else 'unknown'
        if month not in summary:
            summary[month] = 0
        summary[month] += e['amount']
    return summary


def by_category(expenses):
    cats = {}
    for e in expenses:
        cat = e['category'] or 'other'
        if cat not in cats:
            cats[cat] = 0
        cats[cat] += e['amount']
    return cats


def budget_check(expenses, budget):
    total = sum(e['amount'] for e in expenses)
    return {
        "total": total,
        "budget": budget,
        "over_budget": total > budget,
        "remaining": budget - total
    }
