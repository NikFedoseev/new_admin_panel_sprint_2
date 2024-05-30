from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models import Q
from django.contrib.postgres.aggregates import ArrayAgg

from movies.models import Filmwork, PersonFilmwork


class MoviesQuerysetMixin():
    def get_queryset(self):
        return (
            Filmwork.objects.all()
            .prefetch_related('genres', 'persons')
            .values(
                'id', 'title', 'description', 'creation_date', 'rating', 'type'
            )
            .annotate(
                genres=ArrayAgg('genres__name', distinct=True),
                actors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.ACTOR)
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.DIRECTOR)
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=PersonFilmwork.Role.WRITER)
                ),
            )
        )


class MoviesListApi(MoviesQuerysetMixin, BaseListView):
    http_method_names = ['get']
    paginate_by = 50
    model = Filmwork

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        page_size = self.get_paginate_by(queryset)
        paginator, page, queryset, _ = self.paginate_queryset(
            queryset, page_size
        )
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset),
        }

        return context

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesQuerysetMixin, BaseDetailView):
    http_method_names = ['get']

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context['object'])
