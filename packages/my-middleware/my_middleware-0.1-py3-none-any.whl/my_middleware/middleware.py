# my_middleware/middleware.py
from flask import request, jsonify

class MyMiddleware:
    def __init__(self, app):
        self.app = app
        # Register the before_request handler
        self.app.before_request(self.before_request)

    def before_request(self):
        # Apply the middleware check to every route
        check_passed = self.custom_check()
        if not check_passed:
            return jsonify({"error": "Pre-check failed"}), 403

    def custom_check(self):
        print("middleware ran")
        return True
