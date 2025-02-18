# order.py
from db.models import models, Order, Ticket, User
from datetime import datetime
from django.db import transaction


def create_order(
    tickets: list,
    username: str,
    date: datetime = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket in tickets:
            ticket_ = Ticket.objects.create(
                movie_session_id=ticket["movie_session"],
                row=ticket["row"],
                seat=ticket["seat"],
                order=order)
            ticket_.save()

        order.save()

    return order


def get_orders(username: str = None) -> models.QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
