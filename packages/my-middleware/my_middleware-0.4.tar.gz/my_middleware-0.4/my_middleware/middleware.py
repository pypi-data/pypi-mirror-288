# middleware.py

import inspect
from flask import request
from django.http import JsonResponse
from fastapi import Request
from fastapi.responses import JSONResponse

class GeneralMiddleware:
    def __init__(self, get_request_data, respond_with_error, next_handler):
        print("In the constructor of Middleware module")
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler

    def __call__(self, *args, **kwargs):
        print("Call function called from middleware module")

        if inspect.signature(self.get_request_data).parameters:
            # If yes, pass *args and **kwargs
            request_data = self.get_request_data(*args, **kwargs)
        else:
            # If no, call it without arguments
            request_data = self.get_request_data()

        if not self.custom_check(request_data):
            print("Call function completed from middleware module")
            return self.respond_with_error("API check failed", status=403)

        print("Call function completed from middleware module")
        return self.next_handler(*args, **kwargs)

    def custom_check(self, request_data):
        print("In the middleware module")
        print(request_data)
        # Custom logic based on the API response
        return True

def flask_middleware(get_request_data, respond_with_error):
    def decorator(func):
        def wrapper(*args, **kwargs):
            middleware = GeneralMiddleware(get_request_data, respond_with_error, lambda: func(*args, **kwargs))
            return middleware(*args, **kwargs)
        return wrapper
    return decorator

def django_middleware(get_request_data, respond_with_error):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            middleware = GeneralMiddleware(get_request_data, respond_with_error, view_func)
            return middleware(request, *args, **kwargs)
        return wrapper
    return decorator

def fastapi_middleware(get_request_data, respond_with_error, next_handler):
    middleware = GeneralMiddleware(get_request_data, respond_with_error, next_handler)
    
    async def wrapper(request: Request, *args, **kwargs):
        request_data = await request.json()  # Example: retrieve request data for FastAPI
        if not middleware.custom_check(request_data):
            return JSONResponse(content={"error": "API check failed"}, status_code=403)
        return await middleware.next_handler(request, *args, **kwargs)
    
    return wrapper
