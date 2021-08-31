from rest_framework import viewsets, filters, views, status, authentication, permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .models import Film, FilmGenre, FilmUser
from .serializers import FilmSerializer, FilmGenreSerializer, FilmUserSerializer


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
    ordering_fields = ['title', 'year', 'genres__name', 'favorites', 'average_note']
    filterset_fields = {
                        'year': ['lte', 'gte'],  # Year less than or equal to, greater than or equal to
                        'genres': ['exact']      # Exact gender
                        }

class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FilmGenre.objects.all()
    serializer_class = FilmGenreSerializer
    lookup_field = 'slug'  #We will identify the genders using their slug

class FilmUserViewSet(views.APIView):

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    # The GET method will return the user's movies
    def get(self, request, *args, **kwargs):
        queryset = FilmUser.objects.filter(user=self.request.user)
        serializer = FilmUserSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # The POST method will allow you to manage your movie information
    def post(self, request, *args, **kwargs):
        try:
            film = Film.objects.get(id=request.data['uuid'])
        except Film.DoesNotExist:
            return Response(
                {'status': 'Film not found'},
                status=status.HTTP_404_NOT_FOUND)

        # Once the film is recovered, we create or recover its FilmUser
        film_user, created = FilmUser.objects.get_or_create(
            user=request.user, film=film)

        # We configure each field
        film_user.state = request.data.get('state', 0)
        film_user.favorite = request.data.get('favorite', False)
        film_user.note = request.data.get('note', -1)
        film_user.review = request.data.get('review', None)

        # If the movie is marked as NOT VIEWED, we delete it automatically
        if int(film_user.state) == 0:
            film_user.delete()
            return Response(
                {'status': 'Deleted'}, status=status.HTTP_200_OK)

        # Otherwise we save the fields of the user movie
        else:
            film_user.save()

        return Response(
            {'status': 'Saved'}, status=status.HTTP_200_OK)