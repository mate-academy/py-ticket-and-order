from django.db import transaction
from django.db.models import QuerySet

from db.models import Order, User


@transaction.atomic
def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    user = User.objects.get(username=username)
    order = user.orders.create(
        user=user,
    )
    if date:
        order.created_at = date
    order.save()
    for ticket in tickets:
        order.tickets.create(
            row=ticket.get("row"),
            seat=ticket.get("seat"),
            movie_session_id=ticket.get("movie_session"),
        )
    return order


def get_orders(username: str = None) -> QuerySet[Order]:
    query = Order.objects.all()
    if username:
        query = query.filter(user__username=username)
    return query
