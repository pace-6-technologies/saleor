import django_filters

from ..core.filters import BaseJobFilter
from ..core.types import FilterInputObjectType
from ..utils.filters import filter_by_query_param


def filter_user(qs, _, value):
    user_fields = [
        "user__first_name",
        "user__last_name",
        "user__email",
    ]
    qs = filter_by_query_param(qs, value, user_fields)
    return qs


def filter_app(qs, _, value):
    app_fields = [
        "app__name",
    ]
    qs = filter_by_query_param(qs, value, app_fields)
    return qs

def filter_import_type(qs, _, value):
    qs = filter_by_query_param(qs, value, ["import_type"])
    return qs


class ImportFileFilter(BaseJobFilter):
    user = django_filters.CharFilter(method=filter_user)
    app = django_filters.CharFilter(method=filter_app)
    import_type = django_filters.CharFilter(method=filter_import_type)


class ImportFileFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = ImportFileFilter
