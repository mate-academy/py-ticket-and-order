from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.timezone import now


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
    title = models.CharField(max_length=255, db_index=True)  # Adding index
    description = models.TextField()
    actors = models.ManyToManyField(
        to=Actor, related_name="movies"
    )
    genres = models.ManyToManyField(
        to=Genre, related_name="movies"
    )

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
        related_name="movie_sessions",
    )
    movie = models.ForeignKey(
        to=Movie,
        on_delete=models.CASCADE,
        related_name="movie_sessions",
    )

    def __str__(self) -> str:
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(default=now)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")


class Ticket(models.Model):
    movie_session = models.ForeignKey(
        "MovieSession", on_delete=models.CASCADE
    )
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie_session", "row", "seat"],
                name="unique_movie_session_row_seat",
            )
        ]

    def __str__(self) -> str:
        return (
            f"{self.movie_session.movie.title} "
            f"{self.movie_session.show_time} "
            f"(row: {self.row}, seat: {self.seat})"
        )

    def clean(self) -> None:
        """Validate that row and seat numbers are within the allowed range."""
        if self.movie_session_id is None:
            raise ValidationError(
                "Movie session must be set before validation."
            )

        cinema_hall = self.movie_session.cinema_hall

        if self.row < 1 or self.row > cinema_hall.rows:
            raise ValidationError(
                {
                    "row": (
                        f"Row number must be between 1 and {cinema_hall.rows}."
                    )
                }
            )

        if self.seat < 1 or self.seat > cinema_hall.seats_in_row:
            raise ValidationError(
                {
                    "seat": (
                        "Seat number must be between 1 and "
                        f"{cinema_hall.seats_in_row}."
                    )
                }
            )

    def save(self, *args, **kwargs) -> None:
        """Enforce validation before saving."""
        self.full_clean()  # Calls clean() before saving
        super().save(*args, **kwargs)


class User(AbstractUser):
    groups = models.ManyToManyField(
        Group, related_name="custom_user_set", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True,
    )

    def __str__(self) -> str:
        return self.username
