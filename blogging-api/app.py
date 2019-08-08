from flask import Flask, request, jsonify
from database import db
from models import Post
from auth import init_auth_db, register_user, login_user, verify_token

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    init_auth_db()


def get_current_user():
    """Extract and verify user from Authorization header."""
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Bearer '):
        return None
    token = auth[7:]
    return verify_token(token)


@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.json
    try:
        register_user(data['username'], data['password'], data.get('email', ''))
        return jsonify({"message": "registered"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/login', methods=['POST'])
def login():
    """Login and get a token."""
    data = request.json
    token = login_user(data['username'], data['password'])
    if not token:
        return jsonify({"error": "invalid credentials"}), 401
    return jsonify({"token": token})


@app.route('/posts', methods=['GET'])
def list_posts():
    """List all posts, optionally filtered by tag."""
    tag = request.args.get('tag')
    query = Post.query.order_by(Post.created_at.desc())
    if tag:
        # naive tag filtering - contains check on comma-separated string
        query = query.filter(Post.tags.contains(tag))
    posts = query.all()
    return jsonify([p.to_dict() for p in posts])


@app.route('/posts', methods=['POST'])
def create_post():
    """Create a new post. Requires auth."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    if not data.get('title'):
        return jsonify({"error": "title required"}), 400
    tags = ",".join(data.get('tags', []))
    post = Post(
        title=data['title'],
        content=data.get('content', ''),
        author_id=user['user_id'],
        tags=tags,
    )
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "created", "id": post.id}), 201


@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    """Get a post by id."""
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "not found"}), 404
    return jsonify(post.to_dict())


@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    """Delete a post. Requires auth."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "unauthorized"}), 401
    post = Post.query.get(id)
    if not post:
        return jsonify({"error": "not found"}), 404
    if post.author_id != user['user_id']:
        return jsonify({"error": "forbidden"}), 403
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "deleted"})


if __name__ == '__main__':
    app.run(debug=True, port=5002)
