from db.models import Ticket, Order
from django.db.models import QuerySet
from django.db import transaction
from django.contrib.auth import get_user_model


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
