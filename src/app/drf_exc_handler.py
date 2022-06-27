# https://www.django-rest-framework.org/api-guide/exceptions/
"""
Turns errors messages from 400 BAD_REQUEST from this:
{
    "{field_name}": [
        "{error 1}",
        "{error 2}",
    ]
}

To this:

{
    "errors": [
        {
            "messages": [
                "{error 1}",
                "{error 2}",
            ],
            "field": "{field_name}"
        }
    ]
}
"""
from typing import Optional
from rest_framework.response import Response
from rest_framework.views import exception_handler


def make_error_message_on_validation_error(exc, context):
    response: Optional[Response] = exception_handler(exc, context)

    if not response or response.status_code != 400:
        return response

    errors = []
    old_data = response.data
    for field_name, messages in old_data.items():
        if isinstance(messages, dict):
            field_errors = messages.values()
        elif isinstance(messages, str):
            field_errors = [messages]
        elif isinstance(messages, (list, tuple)):
            field_errors = messages
        else:
            return response

        errors.append({"field": field_name, "messages": field_errors})
    response.data = {"errors": errors}

    return response
