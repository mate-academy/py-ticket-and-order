from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket
from typing import Optional

@transaction.atomic
def create_order(tickets: list[dict], username: str, date: Optional[str] = None) -> Order:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()
    for ticket_data in tickets:
        Ticket.objects.create(
            order=order,
            **ticket_data
        )
    return order

def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)
    return orders
