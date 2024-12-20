from datetime import datetime
from typing import Any

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
    tickets: list[dict[str, Any]],
    username: str,
    date: datetime.date = None,
) -> Order:
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        raise ValidationError(
            f"User with username '{username}' does not exist."
        )

    with transaction.atomic():
        order = Order.objects.create(user=user)

        if date:
            created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.created_at = created_at
        order.save()

        for ticket in tickets:
            required_fields = {"row", "seat", "movie_session"}
            if not required_fields.issubset(ticket):
                raise ValidationError("Missing required ticket fields")

            try:
                movie_session = MovieSession.objects.get(
                    id=ticket["movie_session"]
                )
            except MovieSession.DoesNotExist:
                raise ValidationError(
                    f"Movie session with id {ticket['movie_session']} "
                    f"doesn't exist."
                )

            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=movie_session,
                order=order,
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all().order_by("-id")
    if username:
        queryset = queryset.filter(user__username=username).order_by("-id")

    return queryset
