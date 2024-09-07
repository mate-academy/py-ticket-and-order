from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"]),
        ]


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self) -> str:
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(
        to=CinemaHall, on_delete=models.CASCADE,
        related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE,
        related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User",
                             on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-created_at"]


# db/models.py

class Ticket(models.Model):
    movie_session = models.ForeignKey("MovieSession",
                                      on_delete=models.CASCADE)
    order = models.ForeignKey("Order",
                              on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        movie_title = self.movie_session.movie.title
        show_time = self.movie_session.show_time.strftime(
            '%Y-%m-%d %H:%M:%S')
        return (f"{movie_title} {show_time}"
                f" (row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        movie_session = self.movie_session
        if not (1 <= self.row <= movie_session.cinema_hall.rows):
            raise ValidationError({
                "row": f"row number must be in available range:"
                       f" (1, rows): (1,"
                       f" {movie_session.cinema_hall.rows})"
            })
        if not (
                1 <= self.seat <= movie_session.cinema_hall.seats_in_row):
            raise ValidationError({
                "seat": f"seat number must be in available range:"
                        f" (1, seats_in_row): (1,"
                        f" {movie_session.cinema_hall.seats_in_row})"
            })

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "order", "row", "seat"],
                name="unique_ticket"
            )
        ]
