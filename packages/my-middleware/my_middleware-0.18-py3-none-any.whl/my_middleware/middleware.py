import requests
import inspect

class GeneralMiddleware:
    def __init__(self, get_request_data, respond_with_error, next_handler):
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler

    def __call__(self, *args, **kwargs):

        if inspect.signature(self.get_request_data).parameters:
            # If yes, pass *args and **kwargs
            request_data = self.get_request_data(*args, **kwargs)
        else:
            # If no, call it without arguments
            request_data = self.get_request_data()
        if not self.custom_check(request_data):
            return self.respond_with_error("API check failed", status=403)
        return self.next_handler(*args, **kwargs)

    def custom_check(self,request_data):
        
        print(request_data)
        print("In the middleware module")
        # Custom logic based on the API response
        return True
