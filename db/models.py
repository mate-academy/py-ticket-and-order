from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

import settings


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
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    class Meta:
        indexes = [models.Index(fields=["title"])]
        default_related_name = "movies"

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
        to=CinemaHall,
        on_delete=models.CASCADE,

    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = "sessions"

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-created_at"]
        default_related_name = "orders"

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        MovieSession,
        on_delete=models.CASCADE,
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="ticket_unique_constraint"
            )
        ]
        default_related_name = "tickets"

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} {self.movie_session.show_time}"
            f" (row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        cinema_hall_data = self.movie_session.cinema_hall

        if not (1 <= self.row <= cinema_hall_data.rows):
            raise ValidationError(
                {
                    "row": f"row number must be in available range: (1, rows):"
                           f" (1, {cinema_hall_data.rows})"
                }
            )
        if not (1 <= self.seat <= cinema_hall_data.seats_in_row):
            raise ValidationError(
                {
                    "seat": f"seat number must be in available range:"
                            f" (1, seats_in_row):"
                            f" (1, {cinema_hall_data.seats_in_row})"
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class User(AbstractUser):
    pass
