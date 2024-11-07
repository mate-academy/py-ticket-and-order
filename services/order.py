from db.models import Order, Ticket
from django.db.models import QuerySet
from django.db import transaction


def create_order(tickets: list[dict], username, date: str = None) -> Order:
    with transaction.atomic():
        order = Order()
        order.user = username
        if date:
            order.created_at = date
        order.save()
        order_tickets = []
        for ticket in tickets:
            order_ticket = Ticket(*ticket)
            order_ticket.save
            order_tickets.append(order_ticket)
        order.tickets.set(order_tickets)
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user_username=username)
    return queryset
    