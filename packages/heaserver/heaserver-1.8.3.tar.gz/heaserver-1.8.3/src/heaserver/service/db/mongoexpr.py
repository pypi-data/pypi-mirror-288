"""Provides a function for creating mockmongo query expressions from HEA REST API parameters.
"""
from heaobject import user
from aiohttp.web import Request
from typing import Optional
import logging
from copy import deepcopy, copy


def mongo_expr(request: Request, var_parts, mongoattributes=None, extra=None):
    """
    Create and returns a mockmongo query expression representing filter criteria.

    If mongoattributes is a string, then mongoattributes is treated as a mockmongo field name, and var_parts is
    expected to be an aiohttp dynamic resource variable part with the desired value of the field name.

    If var_parts is a string and mongoattributes is not specified or None, the value of var_parts is treated as a
    mongo field name, and it is also an aiohttp dynamic resource variable part with the desired value of the field
    name.

    If mongoattributes is a dict, then it is treated as a mockmongo query expression, and the value of var_parts is ignored.

    If mongoattributes is an iterable of strings, then it is treated as an array of mockmongo field names, and var_parts is
    expected to be an iterable of aiohttp match_info strings with the desired values of the corresponding field names
    in mongoattributes.

    If var_parts is an iterable of strings and mongoattributes is unspecified or None, then it is treated as both an
    iterable of mockmongo field names and corresponding aiohttp dynamic resource variable parts with the desired values of
    the corresponding field names.

    If mongoattributes or var_parts are specified but are neither a dict, an iterable of strings nor a string, a
    TypeError will be raised.

    If mongoattributes and var_parts are both unspecified or None, an empty mockmongo query expression is created.

    If extra is a dict, it will be merged with the query expression dict above, overriding any overlapping parts of the
    expression. If extra is not None and is not a dict, a TypeError will be raised.

    The resulting query expression is returned.

    :param request: the aiohttp request.
    :param var_parts: the names of the dynamic resource's variable parts.
    :param mongoattributes: the attribute(s) to filter by, or a mockmongo query expression.
    :param extra: another mockmongo query expression.
    :return: a dict containing a mockmongo query expression.
    :raises TypeError: as described above.
    """
    logger = logging.getLogger(__name__)
    if isinstance(mongoattributes, str) and isinstance(var_parts, str):
        d = {mongoattributes: request.match_info[var_parts]}
    elif not mongoattributes and isinstance(var_parts, str):
        d = {var_parts: request.match_info[var_parts]}
    elif isinstance(mongoattributes, dict):
        d = copy(mongoattributes)
    elif mongoattributes or var_parts:
        d = {nm: request.match_info[var_parts[idx]]
             for idx, nm in enumerate(mongoattributes if mongoattributes else var_parts)}
    else:
        d = {}
    if extra:
        extra_ = deepcopy(extra)
        if '$or' in extra_ and '$or' in d:
            if '$and' not in d:
                d.update({'$and': [{'$or': extra_.pop('$or')}, {'$or': d.pop('$or')}]})
            else:
                d['$and'].append({'$or': extra_.pop('$or')})
        if '$and' in extra_ and '$and' in d:
            d['$and'].extend(extra_.pop('$and'))
        d.update(extra_)
    logger.debug('Mongo expression is %s', d)
    return d


def sub_filter_expr(sub: Optional[str], permissions=None):
    """
    Returns mongodb expression that filters results by user and permissions.

    :param sub: the user to filter by.
    :param permissions: the permissions to filter by. If None or empty, permissions are not checked.
    :return: a dict.
    """
    return {'$or': [{'owner': sub},
                    {'shares': {
                        '$elemMatch': {
                            'user': {'$in': _matching_users(sub)}
                        } if not permissions else {
                            'user': {'$in': _matching_users(sub)}, 'permissions': {'$elemMatch': {'$in': permissions}}
                        }
                    }}]
            } if sub else None


def _matching_users(sub: str):
    """
    Returns a list containing the provided user and generic system users.

    :param sub: the user.
    :return: a list of users.
    """
    return [sub, user.ALL_USERS]

