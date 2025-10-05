from rest_framework.views import exception_handler


def handler_function(exc, context):
    response = exception_handler(exc, context)

    # Customize only authentication errors
    if response is not None and response.status_code == 401:
        detail = response.data.get("detail")
        response.data.clear()
        response.data["status"] = "failed"
        response.data["detail"] = detail
        response.data["message"] = "Token is either expired or not valid"

    return response
