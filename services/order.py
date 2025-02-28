from datetime import datetime
from db.models import Order, User, Ticket, MovieSession
from django.db.models import QuerySet
from django.db import transaction


def create_order(tickets: list,
                 username: str,
                 date: datetime = None) -> Order:

    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)
        if date:
            order.created_at = date
            order.save()

        ticket_ = []
        for ticket in tickets:
            if not (
                MovieSession.objects.filter(id=ticket["movie_session"])
                .exists()
            ):
                raise ValueError(f"Invalid movie_session_id: "
                                 f"{ticket["movie_session"]}")

            ticket_.append(
                Ticket(movie_session_id=ticket["movie_session"],
                       row=ticket["row"],
                       seat=ticket["seat"],
                       order=order
                       )
            )

        Ticket.objects.bulk_create(ticket_)
    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    else:
        return Order.objects.all()
