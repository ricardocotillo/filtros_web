from django.db.models import Func


class RemoveHyphens(Func):
    function = "REPLACE"
    template = "%(function)s(%(expressions)s, '-', '')"
