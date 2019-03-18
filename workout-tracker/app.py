from flask import Flask
from models import init_db
from routes import workouts_bp

app = Flask(__name__)
app.register_blueprint(workouts_bp)

init_db()

if __name__ == '__main__':
    app.run(debug=True, port=5007)
