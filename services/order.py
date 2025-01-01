from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None,
) -> Order:

    with transaction.atomic():
        order_data = {"user": get_user_model().objects.get(username=username)}
        if date:
            order_data["date"] = date

        order = Order.objects.create(**order_data)

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order=order,
                row=ticket["row"],
                status=ticket["status"]
            )

        return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
