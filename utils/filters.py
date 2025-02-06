from django_filters.rest_framework import (
    NumberFilter, BaseRangeFilter, BaseInFilter, CharFilter
)


class NumberRangeFilter(BaseRangeFilter, NumberFilter):
    pass


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass
