from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, MovieSession, Ticket


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: datetime = None
) -> Order:
    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)
    if date:
        order.created_at = date
        order.save()

    movie_session_ids = {ticket["movie_session"] for ticket in tickets}
    movie_sessions = MovieSession.objects.in_bulk(movie_session_ids)

    if missing_sessions := movie_session_ids - set(movie_sessions.keys()):
        raise ValueError(
            f"Movie sessions with IDs {missing_sessions} do not exist."
        )

    ticket_objects = [
        Ticket(
            row=ticket_data["row"],
            seat=ticket_data["seat"],
            movie_session=movie_sessions[ticket_data["movie_session"]],
            order=order
        )
        for ticket_data in tickets
    ]

    for ticket in ticket_objects:
        ticket.full_clean()
    Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: str = None) -> QuerySet:
    return (
        Order.objects.filter(user__username=username)
        if username else Order.objects.all()
    )
