from datetime import datetime
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket

User = get_user_model()


def create_order(
    tickets: list[dict[str, int]],
    username: str,
    date: Optional[datetime] = None
) -> None:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)

        if date:
            Order.objects.filter(id=order.id).update(created_at=date)

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )

            Ticket.objects.create(
                movie_session=movie_session,
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
