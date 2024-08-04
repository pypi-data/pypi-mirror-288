import requests

class GeneralMiddleware:
    def __init__(self, get_request_data, respond_with_error, next_handler):
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler

    def __call__(self, *args, **kwargs):
        if not self.custom_check():
            return self.respond_with_error("API check failed", status=403)
        return self.next_handler(*args, **kwargs)

    def custom_check(self):
        request_data = self.get_request_data()

        # Hardcoded API URL to check
        api_url = 'http://127.0.0.1:5000/open'

        # Make the API request
        response = requests.get(api_url, headers=request_data)
        print(response)
        # Custom logic based on the API response
        return response.status_code == 200
