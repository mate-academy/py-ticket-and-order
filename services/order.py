from datetime import datetime

from django.db import transaction

from db.models import Order, User, Ticket


def create_order(
        tickets: list[dict[str, int]],
        username: str,
        date: datetime.date = None,
) -> Order:
    user = User.objects.get(username=username)

    with transaction.atomic():
        order = Order.objects.create(user=user)
        if date:
            order.created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
            order.save()

        # Create tickets associated with the order
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session_id=ticket_data["movie_session"]
            )
        return order


def get_order(username: str = None) -> list[Order]:
    if username:
        user = User.objects.get(username=username)
        return list(Order.objects.filter(user=user))
    return list(Order.objects.all())
