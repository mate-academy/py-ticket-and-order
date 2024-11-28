from django.db import transaction
from db.models import Order, Ticket, MovieSession, User

def create_order(tickets, username, date=None):
    user = User.objects.filter(username=username).first()
    if not user:
        return None

    with transaction.atomic():
        order = Order.objects.create(user=user, created_at=date) if date else Order.objects.create(user=user)
        for ticket in tickets:
            Ticket.objects.create(
                movie_session=MovieSession.objects.get(id=ticket["movie_session"]),
                order=order,
                row=ticket["row"],
                seat=ticket["seat"]
            )
        return order

def get_orders(username=None):
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
