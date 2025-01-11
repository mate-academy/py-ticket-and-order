from db.models import Order, Ticket
from django.db import transaction


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(username=username)

        if date:
            order.created_at = date

        order.save()

        tickets = [Ticket(order=order, **ticket) for ticket in tickets]
        Ticket.objects.bulk_create(tickets)


def get_order(username: str = None) -> Order:
    if username:
        return Order.objects.filter(username=username)
    return Order.objects.all()



