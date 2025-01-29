from django.db.models import QuerySet

from db.models import Order
from db.models import Ticket
from db.models import MovieSession
from django.db import transaction
from datetime import datetime
from django.contrib.auth.models import User

def create_order(tickets, username, date=None):
    with transaction.atomic():
        user = User.objects.get(username=username)

        if not date:
            date = datetime.now()

        order = Order.objects.create(user=user, created_at=date)

        for ticket_data in tickets:
            movie_session = MovieSession.objects.get(pk=ticket_data["movie_session"])

            Ticket.objects.create(
                row=ticket_data["row"],
                seat=ticket_data["seat"],
                movie_session=movie_session,
                order=order
            )

    return order

def get_order(username:str = None):
    if username:
        orders = Order.objects.filter(user__username=username)
    else:
        orders = Order.objects.all()

    return orders



