"""Centralized error handlers for Flask apps."""
from flask import jsonify


class NotFoundError(Exception):
    """Resource not found."""
    pass


class ValidationError(Exception):
    """Invalid input data."""
    pass


def register_error_handlers(app):
    """Register error handlers on a Flask app."""

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "not found", "status": 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "method not allowed", "status": 405}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "internal server error", "status": 500}), 500

    @app.errorhandler(NotFoundError)
    def handle_not_found(e):
        return jsonify({"error": str(e), "status": 404}), 404

    @app.errorhandler(ValidationError)
    def handle_validation(e):
        return jsonify({"error": str(e), "status": 400}), 400
