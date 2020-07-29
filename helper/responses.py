def succeess_response(data: list = [], code: int = 200, message: str = "Empty list returned") -> dict:
    return {
        "data": data,
        "code": code,
        "message": message
    }


def error_response(data: list = [], code: int = 400, message: str = "An error occured.") -> dict:
    return {
        "data": data,
        "code": code,
        "message": message
    }