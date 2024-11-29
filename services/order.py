from django.db.models import QuerySet
from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, User, MovieSession


def create_order(tickets: list[dict], username: str, date: str = None) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order_tickets = Order(user=user)
        order_tickets.save()
        if date:
            created_at_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order_tickets.created_at = created_at_date
            order_tickets.save()

        ticket = [
            Ticket(row=ticket["row"],
                   seat=ticket["seat"],
                   movie_session_id=ticket["movie_session"],
                   order=order_tickets)
            for ticket in tickets
            if MovieSession.objects.get(id=ticket["movie_session"])]

        Ticket.objects.bulk_create(ticket)


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
