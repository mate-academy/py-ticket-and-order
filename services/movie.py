from typing import Optional

from django.db.models import QuerySet

from db.models import Movie


def get_movies(title: Optional[str] = None) -> QuerySet[Movie]:
    movies = Movie.objects.all()
    if title:
        movies = movies.filter(title__icontains=title)
    return movies


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)


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
