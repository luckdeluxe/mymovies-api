from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Film, FilmGenre
from .serializers import FilmSerializer, FilmGenreSerializer


class ExtendedPagination(PageNumberPagination):
    page_size = 8

    def get_paginated_response(self, data):

        #We recover the default values
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        #We do a split in the first '/' leaving only the parameters
        if next_link:
            next_link = next_link.split('/')[-1]

        if previous_link:
            previous_link = previous_link.split('/')[-1]

        return Response({
            'count': self.page.paginator.count,
            'num_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'page_size': self.page_size,
            'next_link': next_link,
            'previous_link': previous_link,
            'results': data
        })

class FilmViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    # Paging system
    pagination_class = ExtendedPagination
    
    #Filter system
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['title', 'year']
    ordering_fields = ['title', 'year', 'genres__name']
    filterset_fields = {
                        'year': ['lte', 'gte'],  # Year less than or equal to, greater than or equal to
                        'genres': ['exact']      # Exact gender
                        }

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FilmGenre.objects.all()
    serializer_class = FilmGenreSerializer
    lookup_field = 'slug'  #We will identify the genders using their slug