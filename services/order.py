from db.models import User, Order, Ticket
import datetime
from django.db import transaction


def create_order(tickets: list, username: str, date: str = None) -> Order:
    try:
        user = User.objects.get(username=username)

        if date:
            created_at = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        else:
            created_at = datetime.datetime.now()

        with transaction.atomic():
            order = Order.objects.create(user=user, created_at=created_at)

            for ticket_data in tickets:
                Ticket.objects.create(
                    movie_session_id=ticket_data["movie_session"],
                    order=order,
                    row=ticket_data["row"],
                    seat=ticket_data["seat"]
                )

            return order

    except User.DoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")
