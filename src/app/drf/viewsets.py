from typing import Any

from django.db.models import QuerySet
from rest_framework import serializers, viewsets
from rest_framework.pagination import BasePagination

from . import pagination, utils


class AppViewSet(viewsets.ViewSet):
    def get_valid_query_params(self, srlzr_class: type[serializers.Serializer]):
        return utils.get_valid_request_query_params(request=self.request, srlzr_class=srlzr_class)

    def get_valid_data(self, srlzr_class: type[serializers.Serializer]):
        return utils.get_valid_request_data(request=self.request, srlzr_class=srlzr_class)

    def get_paginated_response(
        self,
        queryset: QuerySet,
        srlzr_class: type[serializers.Serializer],
        srlzr_context: dict[str, Any] | None = None,
        pagination_class: type[BasePagination] | None = None,
    ):
        return pagination.get_paginated_response(
            view=self,
            queryset=queryset,
            serializer_class=srlzr_class,
            extra_context=srlzr_context,
            pagination_class=pagination_class or pagination.LimitOffsetPagination,
        )
