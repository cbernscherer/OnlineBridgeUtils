from flask import request
from math import ceil

def pagination_setup(per_page :int, model):
    page = request.args.get('page', 1, type=int)

    assert per_page > 0
    last_page = ceil(model.query.count() / per_page)

    page = min(page, last_page)
    page = max(page, 1)

    return page, last_page