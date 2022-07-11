from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import UniqueConstraint

import settings


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
        t_f = "%Y-%m-%d %H:%M:%S"
        return f"{self.movie.title} {str(self.show_time.strftime(t_f))}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.created_at}"

    class Meta:
        ordering = ["-id"]


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    movie_session = models.ForeignKey("MovieSession", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.movie_session} " \
               f"(row: {self.row}, seat: {self.seat})"

    def clean(self):
        if self.row > self.movie_session.cinema_hall.rows or self.row < 1:
            raise ValidationError({
                "row": f"row number must be in available range: "
                       f"(1, rows): (1, {self.movie_session.cinema_hall.rows})"
            })
        seats_in_row = self.movie_session.cinema_hall.seats_in_row
        if self.seat > seats_in_row or self.seat < 1:
            raise ValidationError({
                "seat": f"seat number must be in available range: "
                        "(1, seats_in_row): "
                        f"(1, {self.movie_session.cinema_hall.seats_in_row})"
            })

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert,
            force_update,
            using,
            update_fields
        )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="Seat exists in this hall"
            )
        ]


class User(AbstractUser):
    pass
