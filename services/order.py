from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, User
from datetime import datetime
from services.movie_session import get_movie_session_by_id


def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    with transaction.atomic():
        new_order = Order.objects.create(
            user=User.objects.get(username=username)
        )

        if date:
            new_order.created_at = datetime.strptime(
                date,
                "%Y-%m-%d %H:%M"
            )

        new_order.save()

        for ticket in tickets:
            Ticket.objects.create(
                order=new_order,
                movie_session=get_movie_session_by_id(
                    ticket.get("movie_session")
                ),
                row=ticket.get("row"),
                seat=ticket.get("seat")
            )


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user=User.objects.get(username=username))

    return queryset
