from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.timezone import now
from db.models import Order, Ticket, User
from datetime import datetime

from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: datetime = None) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username "
                         f"{username} does not exist.")

    order = Order.objects.create(user=user, created_at=date or now())

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
