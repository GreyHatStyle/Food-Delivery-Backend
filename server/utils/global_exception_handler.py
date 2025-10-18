from rest_framework import status
from rest_framework.response import Response


def api_exception_handler(api_view_method):
    """Wraps the "try/except" block, So that I don't have to write it again and again

    Args:
        api_view_method (def method): API view method/function.
    """

    def wrapper(self, request, *args, **kwargs):
        try:
            return api_view_method(self, request, *args, **kwargs)
        

        except Exception as e:
            return Response(
                {
                    "status": "exception",
                    "reason": str(e),
                    "message": "This request can't be fulfilled yet, if this repeats kindly report to admin, Thanks.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    return wrapper
