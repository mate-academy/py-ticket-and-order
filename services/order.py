from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket


def create_order(tickets: list[Ticket],
                 username: str,
                 date: datetime = None) -> Order:
    with transaction.atomic():
        user = get_user_model().objects.get(username=username)

        new_order = Order.objects.create(user_id=user.id)

        if date:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                order_id=new_order.id,
                seat=ticket["seat"],
                row=ticket["row"],
            )

        return new_order


def get_orders(username: str = None) -> QuerySet:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
