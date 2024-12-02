from django.db import transaction
from django.db.models import QuerySet
from django.utils.dateparse import parse_datetime
from django.utils.timezone import now

from db.models import Order, Ticket, User, MovieSession


@transaction.atomic()
def create_order(
    tickets: list[dict],
    username: str = None,
    date: str = None
) -> None:
    created_at = parse_datetime(date) if date else now()
    order = Order.objects.create(user=User.objects.get(username=username))
    order.created_at = created_at
    order.save()
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=MovieSession.objects.get(
                pk=(ticket.get("movie_session"))
            ),
            seat=ticket.get("seat"),
            row=ticket.get("row"),
            order=order
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user=User.objects.get(username=username))
    return orders
