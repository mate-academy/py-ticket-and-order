from django.db import transaction
from django.contrib.auth.models import User
from typing import List, Dict, Optional
from db.models import Order, Ticket  # Assuming Order and Ticket models exist
from datetime import datetime


def create_order(tickets: List[Dict[str, int]], username: str, date: Optional[str] = None) -> Order:
    """
    Create an order with associated tickets. If a date is provided, set created_at to this date.
    Ensures that either the whole operation completes or nothing is saved.

    :param tickets: List of ticket details (row, seat, movie_session).
    :param username: The username of the user creating the order.
    :param date: (Optional) Creation date for the order.
    :return: The created Order object.
    """
    user = User.objects.get(username=username)
    created_at = datetime.strptime(date, "%Y-%m-%d %H:%M") if date else None

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=created_at) if created_at else Order.objects.create(
            user=user)

        ticket_objects = [
            Ticket(order=order, row=ticket["row"], seat=ticket["seat"], movie_session_id=ticket["movie_session"])
            for ticket in tickets
        ]

        Ticket.objects.bulk_create(ticket_objects)

    return order


def get_orders(username: Optional[str] = None):
    """
    Retrieve all orders or orders for a specific user.

    :param username: (Optional) The username to filter orders by.
    :return: A QuerySet of orders.
    """
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
