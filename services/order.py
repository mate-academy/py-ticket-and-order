import datetime
from typing import List

from django.db import transaction

from db.models import Order, Ticket, User


def create_order(tickets: dict, username: str, date: str = None) -> None:
    with (transaction.atomic()):
        user = User.objects.get(username=username)
        show_time = datetime.datetime(2020, 11, 10, 14, 40)
        order_date = show_time.strptime(date, "%Y-%m-%d %H:%M"
                                        ) if date else None

        order = Order.objects.create(user=user, created_at=order_date)
        order.created_at = order_date
        order.save()

        for ticket_info in tickets:
            row = ticket_info.get("row")
            seat = ticket_info.get("seat")
            movie_session_id = ticket_info.get("movie_session")

            Ticket.objects.create(
                row=row,
                seat=seat,
                movie_session_id=movie_session_id,
                order=order
            )


def get_orders(username: str = None) -> List[Order]:
    if username is not None:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
