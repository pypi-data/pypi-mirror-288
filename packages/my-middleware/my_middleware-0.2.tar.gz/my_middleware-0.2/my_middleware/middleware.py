from typing import Callable, Awaitable, Optional
from starlette.responses import JSONResponse
from fastapi import Request,
import inspect

class GeneralMiddleware:
    def __init__(self, get_request_data: Callable[[], dict], respond_with_error: Callable[[str, int], JSONResponse], next_handler: Callable[..., Awaitable[Optional[JSONResponse]]]):
        print("In the constructor of middleware module")
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler

    async def __call__(self,request:Request, *args, **kwargs):

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
        return await self.next_handler(request,*args, **kwargs)

    def custom_check(self,request_data):
        print("In the middleware module")
        print(request_data)
        
        # Custom logic based on the API response
        return True
