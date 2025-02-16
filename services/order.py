from db.models import Ticket, Order
from django.contrib.auth import get_user_model
from django.db import transaction
from datetime import datetime


def create_order(
    tickets: list[dict],
    username: str,
    date: str = None
) -> Order | None:
    user = get_user_model()
    users = user.objects.get(username=username)

    with transaction.atomic():
        order_data = {"user": users}
        if date:
            order_data["created_at"] = datetime.make_aware(
                datetime.strptime(date, "%Y-%m-%d %H:%M")
            )

        order = Order.objects.create(**order_data)

        ticket_objects = [Ticket(order=order, **ticket) for ticket in tickets]
        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> Order:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
