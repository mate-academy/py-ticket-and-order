from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

import init_django_orm  # noqa: F401
from db.models import Ticket, Order, User


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    try:
        user = get_user_model().objects.get(username=username)
    except User.DoesNotExist:
        raise ValueError("User does not exist")

    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    new_tickets = [
        Ticket(
            movie_session_id=ticket.get("movie_session"),
            seat=ticket.get("seat"),
            row=ticket.get("row"),
            order=order
        )
        for ticket in tickets
    ]

    for ticket in new_tickets:
        ticket.full_clean()

    Ticket.objects.bulk_create(new_tickets)

    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()

    if username:
        queryset = queryset.filter(user__username=username)

    return queryset
