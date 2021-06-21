from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class PagePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 40


class OffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 40
