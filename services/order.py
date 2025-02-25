from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, User
from django.db.models import QuerySet


def create_order(
    tickets: list,
    username: str,
    date: datetime = None,
) -> None:
    with transaction.atomic():
        user = User.objects.get(username=username)

        order = Order.objects.create(user=user)

        if date:
            order.created_at = date
            order.save(update_fields=["created_at"])

        for ticket_data in tickets:
            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"],
                order=order
            )


def get_orders(username: str = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
