import inspect
from flask import request
from django.http import JsonResponse
from fastapi import Request
from fastapi.responses import JSONResponse

class GeneralMiddleware:
    def __init__(self, get_request_data, respond_with_error, next_handler, is_async=False):
        print("In the constructor of Middleware module")
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler
        self.is_async = is_async

    async def __call__(self, *args, **kwargs):
        print("Call function called from middleware module")
        
        if self.is_async:
            request_data = await self._get_request_data_async(*args, **kwargs)
            if not await self._custom_check_async(request_data):
                return await self.respond_with_error("API check failed", status=403)
            return await self.next_handler(*args, **kwargs)
        else:
            request_data = self._get_request_data_sync(*args, **kwargs)
            if not self._custom_check_sync(request_data):
                return self.respond_with_error("API check failed", status=403)
            return self.next_handler(*args, **kwargs)

    def _get_request_data_sync(self, *args, **kwargs):
        if inspect.signature(self.get_request_data).parameters:
            return self.get_request_data(*args, **kwargs)
        else:
            return self.get_request_data()

    async def _get_request_data_async(self, *args, **kwargs):
        if inspect.signature(self.get_request_data).parameters:
            return await self.get_request_data(*args, **kwargs)
        else:
            return await self.get_request_data()

    def _custom_check_sync(self, request_data):
        print("In the middleware module (sync)")
        print(request_data)
        return True

    async def _custom_check_async(self, request_data):
        print("In the middleware module (async)")
        print(request_data)
        return True

def flask_middleware(get_request_data, respond_with_error):
    def decorator(func):
        def wrapper(*args, **kwargs):
            middleware = GeneralMiddleware(get_request_data, respond_with_error, lambda *a, **kw: func(*a, **kw), is_async=False)
            return middleware(*args, **kwargs)
        return wrapper
    return decorator

def django_middleware(get_request_data, respond_with_error):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            middleware = GeneralMiddleware(get_request_data, respond_with_error, view_func, is_async=False)
            return middleware(request, *args, **kwargs)
        return wrapper
    return decorator

def fastapi_middleware(get_request_data, respond_with_error, next_handler):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            middleware = GeneralMiddleware(get_request_data, respond_with_error, next_handler, is_async=True)
            return await middleware(request, *args, **kwargs)
        return wrapper
    return decorator
