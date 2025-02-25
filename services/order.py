import datetime
from django.db import transaction
from django.db.models import QuerySet
from db.models import Ticket, Order, User


@transaction.atomic
def create_order(
        tickets: list[Ticket],
        username: str,
        date: datetime = None
) -> None:
    if date is None:
        date = datetime.datetime.now()
    user = User.objects.get_or_create(username=username)
    order = Order.objects.create(user=user, created_at=date)
    for ticket in tickets:
        Ticket.objects.create(
            movie_session=ticket.movie_session,
            order=order,
            row=ticket.row,
            seat=ticket.seats
        )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()
    return orders.order_by("-created_at")
