from typing import Optional

from django.db import transaction
from django.db.models import QuerySet

from db.models import Movie


def get_movies(
    title: Optional[str] = None,
    genres_ids: Optional[list[int]] = None,
    actors_ids: Optional[list[int]] = None,
) -> QuerySet:
    queryset = Movie.objects.all()

    if title is not None:
        queryset = queryset.filter(title__contains=title)

    if genres_ids is not None:
        queryset = queryset.filter(genres__id__in=genres_ids)

    if actors_ids is not None:
        queryset = queryset.filter(actors__id__in=actors_ids)

    return queryset


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    with transaction.atomic():
        movie = Movie.objects.create(
            title=movie_title,
            description=movie_description,
        )
        if genres_ids is not None:
            movie.genres.set(genres_ids)
        if actors_ids is not None:
            movie.actors.set(actors_ids)

        return movie
