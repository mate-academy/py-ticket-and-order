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
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

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
    cinema_hall = models.ForeignKey(to=CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class User(AbstractUser):
    pass


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-user"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        to=MovieSession, on_delete=models.CASCADE
    )
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    row = models.PositiveSmallIntegerField()
    seat = models.PositiveSmallIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="row_seat_movie_session"
            )
        ]

    def clean(self) -> None:
        c_hall_rows = self.movie_session.cinema_hall.rows
        c_hall_seat = self.movie_session.cinema_hall.seats_in_row
        if self.row < 1 or self.row > c_hall_rows:
            raise ValidationError(
                {
                    "row": f"row number must be in available "
                           f"range: (1, rows): (1, {c_hall_rows})"
                }
            )
        if self.seat < 1 or self.seat > c_hall_seat:
            raise ValidationError(
                {
                    "seat": f"seat number must be in available "
                            f"range: (1, seats_in_row): (1, {c_hall_seat})"
                }
            )

    def save(self, *args, **kwargs) -> None:
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return (f"{self.movie_session.movie.title} "
                f"{self.movie_session.show_time} "
                f"(row: {self.row}, seat: {self.seat})")
