from flask import Flask, request, jsonify
from database import db
from models import Expense

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/expenses', methods=['GET'])
def list_expenses():
    """List expenses with optional date range and category filters."""
    start = request.args.get('start')
    end = request.args.get('end')
    category = request.args.get('category')

    query = Expense.query
    if start:
        query = query.filter(Expense.date >= start)
    if end:
        query = query.filter(Expense.date <= end)
    if category:
        query = query.filter_by(category=category)

    expenses = query.all()
    return jsonify([e.to_dict() for e in expenses])


@app.route('/expenses', methods=['POST'])
def create_expense():
    """Create a new expense."""
    data = request.json
    if not data.get('amount'):
        return jsonify({"error": "amount required"}), 400
    expense = Expense(
        amount=float(data['amount']),
        category=data.get('category', 'other'),
        description=data.get('description', ''),
        date=data.get('date', ''),
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({"message": "created", "id": expense.id}), 201


@app.route('/expenses/<int:id>', methods=['DELETE'])
def delete_expense(id):
    """Delete an expense."""
    expense = Expense.query.get(id)
    if not expense:
        return jsonify({"error": "not found"}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5003)
