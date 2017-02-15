#!/usr/bin/env python
# encoding: utf-8

from math import ceil


def warp_query_page(query, page, per_page=10):
    """
    对请求请求包装
    @param query:
    @type query:
    @param page:
    @type page:
    @param per_page:
    @type per_page:
    @return:
    @rtype:
    """

    result = {
        'test':'hi',
        'total': 0,
        'has_prev': False,
        'has_next': False,
        'prev_num': page - 1,
        'page': page,
        'pages': 0,  # 总数
        'next_num': page + 1,
        'per_page': per_page,
        'items': [],
        'iter_pages': [],
    }
    # result2 = copy.copy(vars(result))
    import copy
    result['items'] = [ copy.copy(vars(row)) for row in query.limit(per_page).offset((page - 1) * per_page).all()]

    if page == 1 and len(result['items']) < per_page:
        total = len(result['items'])
    else:
        total = query.order_by(None).count()
    result['total'] = total
    result['pages'] = int(ceil(result['total'] / float(result['per_page'])))
    result['has_prev'] = result['page'] > 1
    result['has_next'] = result['page'] < result['pages']

    def iter_pages(left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, result['pages'] + 1):
            if num <= left_edge or \
                    (num > result['page'] - left_current - 1 and \
                                 num < result['page'] + right_current) or \
                            num > result['pages'] - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

    result['iter_pages'] = list(iter_pages())
    return result


class Pagination(object):
    """
    兼容 前台老代码数据结构
    can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, query, page, per_page, total, items):
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages"""
        if self.per_page == 0:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists"""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert self.query is not None, 'a query object is required ' \
                                       'for this method to work'
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page"""
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.  The four
        parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:

        .. sourcecode:: html+jinja

            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>…</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
                    (num > self.page - left_current - 1 and \
                                 num < self.page + right_current) or \
                            num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num

