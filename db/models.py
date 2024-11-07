import django.core.exceptions
from django.db.models.constraints import UniqueConstraint
from django.contrib.auth.models import AbstractUser
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
    user = models.ForeignKey("User", related_name="orders", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.created_at
    
    class Meta:
        ordering = ["-created_at"]


class Ticket(models.Model):
    movie_session = models.ForeignKey(MovieSession, related_name="movie_sessions", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name="tickets", on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()
    
    def __str__(self) -> str:
        return f"{self.movie_session.movie.title} {self.movie_session.show_time} (row: {self.row}, seat: {self.seat})"
    
    def clean(self):
        if not (1 <= self.row <= self.movie_session.cinema_hall.row):
            raise django.core.exceptions.ValidationError({"row": f"row must be in range[1, {self.movie_session.cinema_hall.row}], not {self.row}"})
        if not (1 <= self.seat <= self.movie_session.cinema_hall.seats_in_row):
            raise django.core.exceptions.ValidationError({"seat": f"seat must be in range[1, {self.movie_session.cinema_hall.seats_in_row}], not {self.seat}"})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=["row", "seat"], name="unique_row_and_seat")
        ]
    
    
class User(AbstractUser):
    pass
