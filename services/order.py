from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        if date:
            new_order = Order.objects.create(
                user=get_user_model().objects.get(username=username),
                created_at=datetime.strptime(date, "%Y-%m-%d %H:%M"),
            )
        else:
            new_order = Order.objects.create(
                user=get_user_model().objects.get(username=username)
            )

        new_order.save()

        for ticket in tickets:
            new_ticket = Ticket.objects.create(
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]
                ),
                order_id=new_order.id,
                row=ticket["row"],
                seat=ticket["seat"],
            )
            new_ticket.save()


def get_orders(
        username: str = None
) -> QuerySet:
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders
