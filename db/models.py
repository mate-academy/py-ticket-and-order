from typing import Any

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


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
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="title_index")
        ]

    def __str__(self) -> str:
        return self.title


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
        to=CinemaHall, on_delete=models.CASCADE, related_name="movie_sessions"
    )
    movie = models.ForeignKey(
        to=Movie, on_delete=models.CASCADE, related_name="movie_sessions"
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="user"
    )

    def __str__(self) -> str:
        return str(self.created_at)

    class Meta:
        ordering = ["-id"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    row = models.IntegerField()
    seat = models.IntegerField()

    def __str__(self) -> str:
        return (f"{self.movie_session.movie} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")

    def clean(self) -> None:
        if self.seat is not None and self.row is not None:
            if not (1 <= self.row <= self.movie_session.cinema_hall.rows):
                raise ValidationError({
                    "row": ["row number must be in available range: "
                            "(1, rows): "
                            "(1, {})".format(self.movie_session.
                                             cinema_hall.rows)]
                })
            elif not (1 <= self.seat
                      <= self.movie_session.cinema_hall.seats_in_row):
                raise ValidationError({
                    "seat": ["seat number must be in available range"
                             ": (1, seats_in_row): " "(1, {})"
                             .format(self.movie_session.cinema_hall
                                     .seats_in_row)]
                })

    def save(self,
             force_insert: bool = False,
             force_update: bool = False,
             using: Any = None,
             update_fields: Any = None
             ) -> None:
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update,
            using=None,
            update_fields=None
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="unique_ticket_constraint",
                fields=["row", "seat", "movie_session"]
            )
        ]
