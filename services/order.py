from datetime import datetime
from xmlrpc.client import DateTime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: DateTime = None
) -> Order:
    with transaction.atomic():
        user = User.get_with_check(username=username)
        order = Order.objects.create(user=user)
        tickets_to_create = [
            Ticket(
                seat=ticket["seat"],
                row=ticket["row"],
                order=order,
                movie_session=MovieSession.get_with_check(
                    id=ticket["movie_session"])
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(tickets_to_create)
        if date:
            order.created_at = validate_and_convert_date(date)
    return order


def validate_and_convert_date(date: DateTime) -> datetime:
    if isinstance(date, DateTime):
        date = datetime.strptime(date.value, "%Y%m%dT%H:%M:%S")
    elif isinstance(date, str):
        try:
            date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError(
                "Invalid date format. Expected format: 'YYYY-MM-DD HH:MM:SS'"
            )
    elif not isinstance(date, datetime):
        raise TypeError(
            "Expected 'date' to be of type DateTime, str or datetime"
        )
    return date


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.get_with_check(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
