from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


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
    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

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


class Order(models.Model):
    class Meta:
        ordering = ["-created_at"]
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"],
                             name="unique_row_seat_movie_session")
        ]

    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self) -> None:
        if not (0 < self.row < self.movie_session.cinema_hall.rows):
            raise ValidationError(f"Row must be in range from 1 to "
                                  f"{self.movie_session.cinema_hall.rows}. "
                                  f"Not {self.row}")

        if not (0 < self.seat < self.movie_session.cinema_hall.seats_in_row):
            raise ValidationError(
                f"Seat must be in range from 1 to "
                f"{self.movie_session.cinema_hall.seats_in_row}. "
                f"Not {self.seat}")

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.movie_session} (row: {self.row}, seat: {self.seat})"


class User(AbstractUser):
    pass