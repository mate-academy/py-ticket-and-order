from django.db import models
from django.db import transaction
from db.models import Movie
from typing import List


def get_movies(
    genres_ids: List[int] = None,
    actors_ids: List[int] = None,
    title: str = None,
) -> models.QuerySet:

    movies_query = Movie.objects.all()

    if genres_ids:
        movies_query = movies_query.filter(genres__id__in=genres_ids)

    if actors_ids:
        movies_query = movies_query.filter(actors__id__in=actors_ids)

    if title:
        movies_query = movies_query.filter(title__icontains=title)

    return movies_query


def get_movie_by_id(movie_id: int) -> Movie:
    try:
        return Movie.objects.get(id=movie_id)
    except Movie.DoesNotExist:
        return None


@transaction.atomic
def create_movie(
    movie_title: str,
    movie_description: str,
    genres_ids: list = None,
    actors_ids: list = None,
) -> Movie:
    movie = Movie.objects.create(
        title=movie_title,
        description=movie_description,
    )
    if genres_ids:
        movie.genres.set(genres_ids)
    if actors_ids:
        movie.actors.set(actors_ids)

    return movie
