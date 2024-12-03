from django.db import transaction
from db.models import Order, Ticket, User
from django.db.models import QuerySet


@transaction.atomic
def create_order(tickets: list[dict],
                 username: str,
                 date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date)

    for ticket in tickets:
        Ticket.objects.create(
            movie_session_id=ticket["movie_session"],
            order=order,
            row=ticket["row"],
            seat=ticket["seat"],
        )

    return order


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
