from datetime import datetime
from operator import attrgetter
from .queryset import FilteredQueryset


def filter_queryset(lookup_function, queryset, field_name, query):
    FilteredQueryset(list(filter(lambda object: lookup_function(
        query, field_name, object), queryset)))


def startswith(query: str, field_name: str, object):
    return str(getattr(object, field_name)).startswith(str(query))


def istartswith(query: str, field_name: str, object):
    return str(getattr(object, field_name)).casefold().startswith(str(query).casefold())


def endswith(query: str, field_name: str, object):
    return str(getattr(object, field_name)).endswith(str(query))


def iendswith(query: str, field_name: str, object):
    return str(getattr(object, field_name)).casefold().endswith(str(query).casefold())


def contains(query: str, field_name: str, object):
    return str(query) in str(getattr(object, field_name))


def icontains(query: str, field_name: str, object):
    return str(query).casefold() in str(getattr(object, field_name)).casefold()


def gt(query, field_name: str, object):
    return float(getattr(object, field_name)) > float(query)


def gte(query, field_name: str, object):
    return float(getattr(object, field_name)) >= float(query)


def lt(query, field_name: str, object):
    return float(getattr(object, field_name)) < float(query)


def lte(query, field_name: str, object):
    return float(getattr(object, field_name)) <= float(query)


def range(query: list, field_name: str, object):
    return query[0] <= getattr(object, field_name) <= query[1]


def date(query, field_name: str, object):
    if isinstance(query, datetime) & isinstance(getattr(object, field_name), datetime):
        return query.date() == getattr(object, field_name).date()
    else:
        return query == getattr(object, field_name)


def year(query: int, field_name, object):
    return query == getattr(object, field_name).year


def month(query: int, field_name, object):
    return query == getattr(object, field_name).month


def day(query: int, field_name, object):
    return query == getattr(object, field_name).day


def time(query, field_name: str, object):
    if isinstance(query, datetime) & isinstance(getattr(object, field_name), datetime):
        return query.time() == getattr(object, field_name).time()
    else:
        return query == getattr(object, field_name)


def hour(query: int, field_name, object):
    return query == getattr(object, field_name).hour


def minute(query: int, field_name, object):
    return query == getattr(object, field_name).minute


def second(query: int, field_name, object):
    return query == getattr(object, field_name).second


def order_by(queryset, field_name, reverse=False):
    return FilteredQueryset(sorted(queryset, key=attrgetter(field_name), reverse=reverse))
