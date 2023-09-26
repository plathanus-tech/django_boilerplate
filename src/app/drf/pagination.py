from collections import OrderedDict
from typing import Any, Type

from django.conf import settings
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.pagination import BasePagination
from rest_framework.pagination import LimitOffsetPagination as DrfLimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView


class LimitOffsetPagination(DrfLimitOffsetPagination):
    default_limit = settings.API_PAGINATION_DEFAULT_LIMIT
    max_limit = settings.API_PAGINATION_MAX_LIMIT

    def get_paginated_data(self, data):
        return OrderedDict(
            [
                ("limit", self.limit),
                ("offset", self.offset),
                ("count", self.count),
                ("next", self.get_next_link()),
                ("previous", self.get_previous_link()),
                ("results", data),
            ]
        )

    def get_paginated_response(self, data):
        """
        We redefine this method in order to return `limit` and `offset`.
        This is used by the frontend to construct the pagination itself.
        """
        return Response(
            OrderedDict(
                [
                    ("limit", self.limit),
                    ("offset", self.offset),
                    ("count", self.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


def get_paginated_response(
    *,
    view: APIView,
    queryset: QuerySet[Any],
    serializer_class: Type[serializers.Serializer],
    extra_context: dict[str, Any] | None = None,
    pagination_class: Type[BasePagination] = LimitOffsetPagination,
) -> Response:
    if not queryset.ordered:
        raise TypeError(
            "Paginating an queryset that's not ordered leads to inconsistent pages.",
            "Add an `order_by` clause to the queryset",
        )
    paginator = pagination_class()

    request = view.request
    page = paginator.paginate_queryset(queryset, request, view=view)

    extra_context = extra_context or {}
    serializer_kwargs = {
        "many": True,
        "context": {"request": request, **extra_context},
    }
    if page is not None:
        serializer = serializer_class(page, **serializer_kwargs)
        return paginator.get_paginated_response(serializer.data)
    serializer = serializer_class(queryset, **serializer_kwargs)

    return Response(data=serializer.data)
