from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


class User(AbstractUser):
    class Meta:
        db_table = 'db_user'


    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

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
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")

    class Meta:
        ordering = ["-created_at"]  # Orders from newest to oldest

    def __str__(self) -> str:
        return f"<Order: {self.created_at}>"


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, on_delete=models.CASCADE, related_name="tickets")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="tickets")
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["movie_session", "row", "seat"], name="unique_ticket_per_session")
        ]

    def __str__(self) -> str:
        return f"<Ticket: {self.movie_session} (row: {self.row}, seat: {self.seat})>"

    def clean(self):
        max_rows = self.movie_session.cinema_hall.rows
        max_seats_in_row = self.movie_session.cinema_hall.seats_in_row

        if not (1 <= self.row <= max_rows):
            raise ValidationError({"row": f"row number must be in available range: (1, rows): (1, {max_rows})"})
        if not (1 <= self.seat <= max_seats_in_row):
            raise ValidationError({"seat": f"seat number must be in available range: (1, seats_in_row): (1, {max_seats_in_row})"})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)