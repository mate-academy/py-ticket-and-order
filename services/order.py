from typing import List, Optional

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone
from datetime import datetime

from db.models import User, Order, MovieSession, Ticket


@transaction.atomic
def create_order(tickets: List[dict],
                 username: str, date: Optional[str] = None) -> None:

    user = User.objects.get(username=username)

    order = Order.objects.create(user=user)

    if date:
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = timezone.now()

    order.created_at = created_at
    order.save()

    for ticket_data in tickets:
        movie_session = MovieSession.objects.get(
            id=ticket_data["movie_session"])
        Ticket.objects.create(
            movie_session=movie_session,
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
