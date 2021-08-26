from rest_framework import serializers
from .models import Film, FilmGenre


class FilmGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmGenre
        fields = '__all__'

    class NestedFilmSerializer(serializers.ModelSerializer):

        class Meta:
            model = Film
            fields = ['id', 'title', 'image_thumbnail', 'genres']


    films = NestedFilmSerializer(many=True, source="film_genres")

class FilmSerializer(serializers.ModelSerializer):

    class Meta:
        model = Film
        fields = '__all__'

    class NestedFilmGenreSerializer(serializers.ModelSerializer):

        class Meta:
            model = FilmGenre
            fields = '__all__'

    genres = NestedFilmGenreSerializer(many=True)