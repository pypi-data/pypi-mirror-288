from .middleware import GeneralMiddleware


def apply_middleware(get_request_data, respond_with_error, next_handler):
    middleware = GeneralMiddleware(get_request_data, respond_with_error, next_handler)
    return middleware
