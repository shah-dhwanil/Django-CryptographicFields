from datetime import datetime, date as date_, time as time_
from operator import attrgetter
from typing import Any, Callable, Tuple, Union
from django.db.models.query import QuerySet
from re import Pattern
from copy import deepcopy


def sort(queryset: QuerySet, lookup_function: Callable[[Union[str, int, float, datetime, date_, time_, Any], str, Any], bool], field_name: str, query: Any) -> QuerySet:
    """
    Filters queryset

    Filters queryset as per lookup provided by user &query provided by user

    :param lookup_function: Functions that filters the data
    :type lookup_function: Callable[[Union[str,int,float,datetime,date,time,Any],str,Any],bool]
    :param queryset: Queryset generated by querying data 
    :type queryset: QuerySet
    :param field_name: Name of the field which is to be filtered 
    :type field_name: str
    :param query: Query for filtering the Queryset
    :type query: Any
    :return: QuerySet with Filtered Data
    :rtype: QuerySet
    """
    queryset = deepcopy(queryset)
    setattr(queryset, '_result_cache', list(filter(lambda object: lookup_function(
        query, field_name, object), queryset)))
    return queryset

def order_by(queryset: QuerySet, field_name: Tuple[str, ...], reverse: bool = False) -> QuerySet:
    """
    Order Queryset by the given field

    Order the Queryset as per field_name given.It supports multiple level of odering

    :param queryset: Queryset generated by querying data
    :type queryset: QuerySet
    :param field_name: Tuple with name of the field from higher priority to lower priority
    :type field_name: Tuple
    :param reverse: Type of ordering (Ascending|Descending), defaults to False
    :type reverse: bool, optional
    :return: QuerySet with Ordered Data
    :rtype: QuerySet
    """
    queryset = deepcopy(queryset)
    setattr(queryset, '_result_cache', sorted(
        queryset, key=attrgetter(*field_name), reverse=reverse))
    return queryset

def startswith(query: str, field_name: str, object: Any) -> bool:
    """
    Check if a string is Starts With the query (Case Sensitive)
    """
    return str(getattr(object, field_name)).startswith(str(query))


def istartswith(query: str, field_name: str, object: Any) -> bool:
    """
    Check if a string is Starts With the query (Not Case Sensitive)
    """
    return str(getattr(object, field_name)).casefold().startswith(str(query).casefold())


def endswith(query: str, field_name: str, object: Any) -> bool:
    """
    Check if a string is Ends With the query (Case Sensitive)
    """
    return str(getattr(object, field_name)).endswith(str(query))


def iendswith(query: str, field_name: str, object: Any) -> bool:
    """
    Check if a string is Ends With the query (Not Case Sensitive)
    """
    return str(getattr(object, field_name)).casefold().endswith(str(query).casefold())


def contains(query: str, field_name: str, object: Any) -> bool:
    """
    Check if query is in value of the object (Case Sensitive)
    """
    return str(query) in str(getattr(object, field_name))


def icontains(query: str, field_name: str, object: Any) -> bool:
    """
    Check if query is in value of the object (Not Case Sensitive)
    """
    return str(query).casefold() in str(getattr(object, field_name)).casefold()


def gt(query: Union[int, float], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return float(getattr(object, field_name)) > float(query)


def gte(query: Union[int, float], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return float(getattr(object, field_name)) >= float(query)


def lt(query: Union[int, float], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return float(getattr(object, field_name)) < float(query)


def lte(query: Union[int, float], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return float(getattr(object, field_name)) <= float(query)


def range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return query[0] < getattr(object, field_name) < query[1]


def _datetime_gt(query: Union[int, Union[date_, datetime, time_]], value: Union[int, Union[date_, datetime, time_]]) -> bool:
    return value > query


def _datetime_gte(query: Union[int, Union[date_, datetime, time_]], value: Union[int, Union[date_, datetime, time_]]) -> bool:
    return value >= query


def _datetime_lt(query: Union[int, Union[date_, datetime, time_]], value: Union[int, Union[date_, datetime, time_]]) -> bool:
    return value < query


def _datetime_lte(query: Union[int, Union[date_, datetime, time_]], value: Union[int, Union[date_, datetime, time_]]) -> bool:
    return value <= query


def _datetime_range(query: Tuple[Union[int, Union[date_, datetime, time_]], Union[int, Union[date_, datetime, time_]]], value: Union[int, Union[date_, datetime, time_]]) -> bool:
    return query[0] < value < query[1]


def date(query: Union[date_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is equal to query
    """
    value = getattr(object, field_name)
    query = query if type(query) == date_ else query.date()
    value = value if type(value) == date_ else value.date()
    return query == value


def date_lt(query: Union[date_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == date_ else query.date()
    value = value if type(value) == date_ else value.date()
    return _datetime_lt(query, value)


def date_lte(query: Union[date_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == date_ else query.date()
    value = value if type(value) == date_ else value.date()
    return _datetime_lte(query, value)


def date_gt(query: Union[date_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == date_ else query.date()
    value = value if type(value) == date_ else value.date()
    return _datetime_gt(query, value)


def date_gte(query: Union[date_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == date_ else query.date()
    value = value if type(value) == date_ else value.date()
    return _datetime_gte(query, value)


def date_range(query: Tuple[Union[date_, datetime], Union[date_, datetime]], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    value = getattr(object, field_name)
    query[0] = query[0] if type(query[0]) == date_ else query[0].date()
    query[1] = query[1] if type(query[1]) == date_ else query[1].date()
    value = value if type(value) == date_ else value.date()
    return _datetime_range(query, value)


def year(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).year


def year_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).year)


def year_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).year)


def year_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).year)


def year_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).year)


def year_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).year)


def month(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).month


def month_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).month)


def month_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).month)


def month_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).month)


def month_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).month)


def month_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).month)


def day(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).day


def day_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).day)


def day_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).day)


def day_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).day)


def day_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).day)


def day_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).day)


def time(query: Union[time_, datetime], field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    value = getattr(object, field_name)
    query = query if type(query) == time_ else query.time()
    value = value if type(value) == time_ else value.time()
    return query == value


def time_lt(query: Union[time_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == time_ else query.time()
    value = value if type(value) == time_ else value.time()
    return _datetime_lt(query, value)


def time_lte(query: Union[time_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == time_ else query.time()
    value = value if type(value) == time_ else value.time()
    return _datetime_lte(query, value)


def time_gt(query: Union[time_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == time_ else query.time()
    value = value if type(value) == time_ else value.time()
    return _datetime_gt(query, value)


def time_gte(query: Union[time_, datetime], field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    value = getattr(object, field_name)
    query = query if type(query) == time_ else query.time()
    value = value if type(value) == time_ else value.time()
    return _datetime_gte(query, value)


def time_range(query: Tuple[Union[time_, datetime], Union[time_, datetime]], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    value = getattr(object, field_name)
    query[0] = query[0] if type(query[0]) == time_ else query[0].time()
    query[1] = query[1] if type(query[1]) == time_ else query[1].time()
    value = value if type(value) == time_ else value.time()
    return _datetime_range(query, value)


def hour(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).hour


def hour_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).hour)


def hour_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).hour)


def hour_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).hour)


def hour_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).hour)


def hour_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).hour)


def minute(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).minute


def minute_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).minute)


def minute_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).minute)


def minute_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).minute)


def minute_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).minute)


def minute_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).minute)


def second(query: int, field_name: str, object: Any) -> bool:
    """
    Checks if value of object is equal to query
    """
    return query == getattr(object, field_name).second


def second_lt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than value of query
    """
    return _datetime_lt(query, getattr(object, field_name).second)


def second_lte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is less than or equal to value of query
    """
    return _datetime_lte(query, getattr(object, field_name).second)


def second_gt(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than value of query
    """
    return _datetime_gt(query, getattr(object, field_name).second)


def second_gte(query: int, field_name: str, object: Any) -> bool:
    """
    Check if value of object is greater than or equal to value of query
    """
    return _datetime_gte(query, getattr(object, field_name).second)


def second_range(query: Tuple[int, int], field_name: str, object: Any) -> bool:
    """
    Check if value of object is in range of query
    """
    return _datetime_range(query, getattr(object, field_name).second)


def regex(query: Pattern, field_name: str, object: Any) -> bool:
    """
    Checks if query pattern is present in value of object
    """
    return bool(list(query.findall(str(getattr(object, field_name)))))
