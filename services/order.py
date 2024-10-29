from db.models import Order, Ticket, User
from django.db import transaction
from django.utils import timezone


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> None:
    with transaction.atomic():
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User does not exist")

        created_at = date if date else timezone.now()

        order = Order.objects.create(user=user, created_at=created_at)

        for ticket in tickets:
            Ticket.objects.create(
                row=ticket["row"],
                seat=ticket["seat"],
                movie_session_id=ticket["movie_session"],
                order=order
            )

def get_orders(
        username: str = None
) -> list:
    if username:
        return Order.objects.all().filter(user__username=username)

    return Order.objects.all()
