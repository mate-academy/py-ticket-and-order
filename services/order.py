from django.contrib.auth import get_user_model
from django.db import transaction
from db.models import Ticket, Order, User


def create_order(tickets: list,
                 username: str,
                 date: str = None) -> Order:
    with transaction.atomic():
        # Перевірка на існування користувача
        try:
            user = get_user_model().objects.get(username=username)
        except User.DoesNotExist:
            raise ValueError("User does not exist")

        order = Order.objects.create(user=user)
        # Встановлення дати створення
        if date:
            order.created_at = date
            order.save()

        # Створення квитків
        for ticket_data in tickets:
            Ticket.objects.create(
                order=order,
                movie_session_id=ticket_data["movie_session"],
                row=ticket_data["row"],
                seat=ticket_data["seat"]
            )

        return order


def get_orders(username: str = None) -> Order:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
