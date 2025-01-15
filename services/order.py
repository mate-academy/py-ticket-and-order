from datetime import datetime

from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User, Ticket, MovieSession


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    order = Order.objects.create(user=User.objects.get(username=username))

    if date:
        order_date = datetime.strptime(date, "%Y-%m-%d %H:%M")
        order.created_at = order_date
        order.save()

    for ticket in tickets:
        new_ticket = Ticket(
            order=order,
            movie_session=MovieSession.objects.get(
                id=ticket.get("movie_session")
            ),
            row=ticket.get("row"),
            seat=ticket.get("seat")
        )
        new_ticket.save()


def get_orders(username: str = None) -> QuerySet:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
