from django_filters.rest_framework import (
    NumberFilter, BaseRangeFilter, BaseInFilter,
)


class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class NumberInFilter(BaseInFilter, NumberFilter):
    pass
