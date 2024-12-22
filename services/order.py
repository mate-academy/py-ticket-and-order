from datetime import datetime

from django.db import transaction

from db.models import Ticket, Order, User, MovieSession


def create_order(tickets: list,
                 username: str,
                 date: datetime = None) -> Ticket:
    with transaction.atomic():
        ticket_objects = []
        user, user_created = User.objects.get_or_create(username=username)
        order, order_created = Order.objects.get_or_create(user=user)
        if date:
            order.created_at = date
            order.save()
        for ticket in tickets:
            row = ticket["row"]
            seat = ticket["seat"]
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"])
            ticket_objects.append(Ticket(
                movie_session=movie_session,
                order=order,
                row=row,
                seat=seat
            ))
        return Ticket.objects.bulk_create(ticket_objects)


def get_orders(username: str = None) -> Order:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all().order_by("-user")
