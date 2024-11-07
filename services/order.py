from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User, MovieSession


def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    with transaction.atomic():
        order = Order()
        user = User.objects.get(username=username)
        order.user = user
        if date:
            order.save()
            order.created_at = date
        order.save()
        session_id = tickets[0].get("movie_session")
        movie_session = MovieSession.objects.get(id=session_id)
        for ticket in tickets:
            order_ticket = Ticket()
            order_ticket.movie_session = movie_session
            order_ticket.row = ticket.get("row")
            order_ticket.seat = ticket.get("seat")
            order_ticket.order = order
            order_ticket.save()
    return order


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
