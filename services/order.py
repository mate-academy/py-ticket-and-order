from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, Ticket, MovieSession
from typing import Optional


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: Optional[str] = None
) -> QuerySet[Order]:
    user = get_user_model().objects.get(username=username)
    order = Order.objects.create(user=user)

    if date:
        order.created_at = date
        order.save()

    for ticket_data in tickets:
        movie_session_id = ticket_data.pop("movie_session")
        movie_session = MovieSession.objects.get(id=movie_session_id)

        Ticket.objects.create(
            order=order,
            movie_session=movie_session,
            **ticket_data
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet[Order]:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset.order_by("-user__username")
