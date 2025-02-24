from typing import List, Dict, Optional
from django.utils.timezone import make_aware
from datetime import datetime
from django.db import transaction
from db.models import Order, Ticket, MovieSession, User


def create_order(
    tickets: List[Dict[str, int]], username: str, date: Optional[str] = None
) -> Order:
    with transaction.atomic():
        user = User.objects.get(username=username)
        order = Order.objects.create(user=user)

        if date:
            order.created_at = make_aware(
                datetime.strptime(date, "%Y-%m-%d %H:%M")
            )
            order.save()

        ticket_objects = [
            Ticket(
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session=MovieSession.objects.get(
                    id=ticket["movie_session"]),
            )
            for ticket in tickets
        ]
        Ticket.objects.bulk_create(ticket_objects)

        return order


def get_orders(username: Optional[str] = None) -> List[Order]:
    orders = Order.objects.all()
    if username:
        orders = orders.filter(user__username=username)

    return list(orders)
