class GeneralMiddleware:
    def __init__(self, get_request_data, respond_with_error, next_handler):
        self.get_request_data = get_request_data
        self.respond_with_error = respond_with_error
        self.next_handler = next_handler
        self.required_key = 'Authorization'  # Hardcoded key to check for

    def __call__(self, *args, **kwargs):
        if not self.custom_check():
            return self.respond_with_error(f"Missing required key: {self.required_key}", status=400)
        return self.next_handler(*args, **kwargs)

    def custom_check(self):
        request_data = self.get_request_data()
        # Check if the required key is present in the request data
        return self.required_key in request_data
