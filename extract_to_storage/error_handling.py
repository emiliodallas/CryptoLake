class APIUnauthorizedError(Exception):
    pass

class APIRateLimitExceededError(Exception):
    pass

class BadRequest(Exception):
    pass

class Unauthorized(Exception):
    pass

class PaymentRequired(Exception):
    pass

class Forbidden(Exception):
    pass

class InternalServerError(Exception):
    pass

def errors(id):
    if id == 401:
        raise APIUnauthorizedError("API key is unauthorized.")
    elif id == 429:
        raise APIRateLimitExceededError("API rate limit exceeded.")
    elif id == 400:
        raise BadRequest("Bad Request.")
    elif id == 401:
        raise Unauthorized("Unauthorized.")
    elif id == 402:
        raise PaymentRequired("Payment Required.")
    elif id == 403:
        raise Forbidden("Forbidden.")
    elif id == 500:
        raise InternalServerError("Internal Server Error.")