from datetime import datetime
from django.db import transaction
from django.contrib.auth import get_user_model
from db.models import Order, Ticket
from django.db.models import QuerySet


def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user = get_user_model().objects.get(username=username)

    if date:
        order_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    else:
        order_date = None

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=order_date)

        ticket_objects = []
        for ticket in tickets:
            movie_session = ticket.get("movie_session")
            row = ticket.get("row")
            seat = ticket.get("seat")

            ticket_objects.append(
                Ticket(
                    order=order,
                    movie_session_id=movie_session,
                    row=row,
                    seat=seat
                )
            )

        for ticket in ticket_objects:
            ticket.full_clean()

        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
