from typing import Optional
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import transaction

from db.models import Order, Ticket


def create_order(tickets: list[dict],
                 username: str,
                 date: Optional = None) -> Order:
    user = get_user_model().objects.get(username=username)

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d %H:%M")
    else:
        date = (datetime.strptime(date, "%Y-%m-%d %H:%M")
                .strftime("%Y-%m-%d %H:%M"))

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date)

        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

        return order


def get_orders(username: Optional[str] = None) -> list[Order]:
    if username:
        user = get_user_model().objects.get(username=username)
        return Order.objects.filter(user=user)
    else:
        return Order.objects.all()
