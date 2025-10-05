"""
This file will have all imports I need in this view
"""

import logging

from rest_framework import status
from rest_framework.response import Response

logger = logging.getLogger("account")


def api_exception_handler(api_view_method):
    """Wraps the "try/except" block, So that I don't have to write it again and again

    Args:
        api_view_method (def method): API view method/function.
    """

    def wrapper(self, request, *args, **kwargs):
        try:
            return api_view_method(self, request, *args, **kwargs)

        except ValueError as ve:
            ve = str(ve)
            detail_for_user = ""

            if ("pydantic" in ve) and ("Value error, " in ve):
                start_index = ve.find("Value error, ") + len("Value error, ")
                end_index = ve.find(" [type=value_error")

                detail_for_user = ve[start_index:end_index]

            else:
                detail_for_user = ""

            return Response(
                {
                    "status": "error",
                    "reason": ve,
                    "message": detail_for_user,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

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
