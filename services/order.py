from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str, date: str = None
) -> Order:

    user = get_user_model().objects.get(username=username)
    with transaction.atomic():
        new_order = Order.objects.create(
            user=user
        )
        if date is not None:
            new_order.created_at = date
            new_order.save()

        for ticket in tickets:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )
            Ticket.objects.create(
                order=new_order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"]
            )


def get_orders(username: str = None) -> QuerySet[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
