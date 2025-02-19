from django.db.models import QuerySet
from django.db import transaction

from db.models import Order, User, Ticket, MovieSession


def create_order(tickets: list, username: str, date: str = None) -> None:
    with transaction.atomic():
        order = Order.objects.create(
            user=User.objects.get(username=username),
            created_at=date)
        if date:
            order.created_at = date
            order.save()
        tickets_to_create = []

        movie_session_ids = [ticket["movie_session"] for ticket in tickets]
        sessions = {s.id: s for s in
                    MovieSession.objects.filter(id__in=movie_session_ids)}

        for ticket in tickets:
            tickets_to_create.append(Ticket(
                movie_session=sessions[ticket["movie_session"]],
                order=order,
                row=ticket["row"],
                seat=ticket["seat"],
            ))

        return Ticket.objects.bulk_create(tickets_to_create)


def get_orders(username: str = None) -> QuerySet:
    queryset = Order.objects.all()
    if username:
        queryset = queryset.filter(user=User.objects.get(username=username))

    return queryset
