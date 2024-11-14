from django.db import transaction
from db.models import Order, Ticket, User
from django.utils import timezone


@transaction.atomic
def create_order(tickets: list[dict], username: str, date: str = None) -> Order:
    user = User.objects.get(username=username)
    order = Order.objects.create(user=user, created_at=date if date else timezone.now())

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: str = None):
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user__username=username)
    return queryset
