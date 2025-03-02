import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from db.models import Ticket, Order


def create_order(
    tickets: list[dict], username: str, date: datetime.datetime = None
) -> Order:
    with transaction.atomic():
        user = get_object_or_404(get_user_model(), username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket["movie_session"],
                seat=ticket["seat"],
                row=ticket["row"],
            )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
