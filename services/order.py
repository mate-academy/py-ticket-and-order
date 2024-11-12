from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.datetime_safe import datetime

from db.models import Order, User, Ticket


def create_order(tickets: list, username: str, date: datetime = None) -> Order:
    if not tickets:
        raise Exception("No tickets to create")

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
        order.save()

        create_tickets = [
            Ticket(
                row=ticket.get("row"),
                seat=ticket.get("seat"),
                movie_session_id=ticket.get("movie_session"),
                order=order
            )
            for ticket in tickets
        ]

        for ticket in create_tickets:
            try:
                ticket.full_clean()
            except ValidationError as e:
                raise ValueError(f"Invalid ticket data: {e}")

        Ticket.objects.bulk_create(create_tickets)

    return order


def get_orders(username: str = None) -> list:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
