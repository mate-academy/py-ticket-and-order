from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint


class Genre(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor)
    genres = models.ManyToManyField(to=Genre)

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["title"])
        ]


class CinemaHall(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class MovieSession(models.Model):
    show_time = models.DateTimeField()
    cinema_hall = models.ForeignKey(to=CinemaHall, on_delete=models.CASCADE)
    movie = models.ForeignKey(to=Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie.title} {str(self.show_time)}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession,
                                      on_delete=models.CASCADE)
    order = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat", "movie_session"],
                             name="unique_place_movie_session")
        ]

    def __str__(self):
        return f"{self.movie_session.movie.title} " \
               f"{self.movie_session.show_time} " \
               f"(row: {self.row}, seat: {self.seat})"

    def clean(self):
        max_rows = self.movie_session.cinema_hall.rows
        max_seats = self.movie_session.cinema_hall.seats_in_row
        row_error_message = f"row number must be in available range: " \
                            f"(1, rows): (1, {max_rows})"
        seats_error_message = f"seat number must be in available range: " \
                              f"(1, seats_in_row): (1, {max_seats})"

        if not (1 <= self.row <= max_rows):
            raise ValidationError({
                "row": row_error_message
            })
        if not (1 <= self.seat <= max_seats):
            raise ValidationError({
                "seat": seats_error_message
            })

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


class User(AbstractUser):
    pass
