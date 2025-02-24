from django.db import transaction
from django.db.models import QuerySet
from db.models import Movie


def get_movies(
    genres_ids: list[int] = None,
    actors_ids: list[int] = None, title: str = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if genres_ids:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids:
        queryset = queryset.filter(actors__id__in=actors_ids)

    if title:
        queryset = queryset.filter(title__icontains=title)

    return queryset.distinct()


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(title: str,
                 description: str,
                 genres: list[int],
                 actors: list[int]) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(title=title,
                                     description=description)
        movie.genres.set(genres)
        movie.actors.set(actors)

    return movie
