from datetime import datetime

from django.db.models import QuerySet
from django.utils.translation.trans_real import translation

from db.models import Order, Ticket


def create_order(tickets: list[dict], username: str, date: datetime) -> list[dict]:
    with translation.atomic():
        order = Order.objects.create(username=username, created_at=date)
        for ticket in tickets:
            Ticket.objects.create(row=ticket["row"],
                              seat=ticket["seat"],
                              movie_session=ticket["movie_session"],
                              order=order)


def get_orders(username: str = None) -> QuerySet[Order]:
    if username:
        return Order.objects.filter(username=username)
    if username is None:
        return Order.objects.all()
