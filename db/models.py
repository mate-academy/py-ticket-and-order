from django.conf import settings
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
    title = models.CharField(max_length=255)
    description = models.TextField()
    actors = models.ManyToManyField(to=Actor, related_name="movies")
    genres = models.ManyToManyField(to=Genre, related_name="movies")

    class Meta:
        indexes = [
            models.Index(fields=["title"], name="movie_title_idx")
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


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="orders")

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.created_at}"


class Ticket(models.Model):
    movie_session = models.ForeignKey(to=MovieSession,
                                      on_delete=models.CASCADE,
                                      related_name="tickets")
    order = models.ForeignKey(to=Order,
                              on_delete=models.CASCADE,
                              related_name="tickets")
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["row", "seat", "movie_session"],
                name="uniq_ticket"
            )
        ]

    def __str__(self) -> str:
        return (f"{self.movie_session} "
                f"(row: {self.row}, seat: {self.seat})")

    @staticmethod
    def validation_param(min_value: int,
                         value: int,
                         max_value: int,
                         param_name: str,
                         field_name: str) -> None:
        if not min_value < value <= max_value:
            raise ValidationError(
                {param_name: [f"{param_name} number must "
                              f"be in available range: "
                              f"({min_value}, {field_name}): ({min_value}, "
                              f"{max_value})"]}
            )

    def clean(self) -> None:
        self.validation_param(1,
                              self.row,
                              self.movie_session.cinema_hall.rows,
                              "row",
                              "rows")
        self.validation_param(1,
                              self.seat,
                              self.movie_session.cinema_hall.seats_in_row,
                              "seat",
                              "seats_in_row")

    def save(self,
             force_insert: bool = False,
             force_update: bool = False,
             using: str = None,
             update_fields: str = None) -> None:
        self.full_clean()
        return super(Ticket, self).save(force_insert=force_insert,
                                        force_update=force_update,
                                        using=using,
                                        update_fields=update_fields)


class User(AbstractUser):
    pass
