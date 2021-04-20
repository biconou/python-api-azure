def response_200(data, message):
    print(data)
    return {"data": data, "code": 200, "message": message}


def response_error(error, code, message):
    return {"error": error, "code": code, "message": message}
