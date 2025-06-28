from datetime import timedelta

from django.urls import reverse

from .tasks import send_reservation_email


def build_reservation_mail(reservation, action, request=None):
    relative_url = reverse('restaurant:reservation_update', args=[reservation.pk])
    url = request.build_absolute_uri(relative_url) if request else relative_url
    name = reservation.owner.get_full_name()

    if action == 'created':
        subject = 'НОВЫЙ РЕЗЕРВ!!!'
        body = (
            f'НОВЫЙ РЕЗЕРВ!\n\n'
            f'Дата: {reservation.date}\n'
            f'Время: {reservation.time}\n'
            f'Гость: {name} - {reservation.owner}\n'
            f'Столик №{reservation.table}\n'
            f'Комментарий: {reservation.comment}\n'
            f'Ссылка для подтверждения: {url}'
        )

    elif action == 'updated':
        subject = 'ИЗМЕНЕНИЕ РЕЗЕРВА!!!'
        body = (
            f'ИЗМЕНЕНИЯ РЕЗЕРВА!\n\n'
            f'Дата: {reservation.date}\n'
            f'Время: {reservation.time}\n'
            f'Гость: {name} - {reservation.owner}\n'
            f'Столик №{reservation.table}\n'
            f'Комментарий: {reservation.comment}\n'
            f'Ссылка для подтверждения: {url}'
        )

    elif  action == 'deleted':
        subject = 'РЕЗЕРВ БЫЛ ОТМЕНЁН!!!'
        body = (
            f'ОТМЕНА РЕЗЕРВА!\n\n'
            f'Дата: {reservation.date}\n'
            f'Время: {reservation.time}\n'
            f'Гость: {name} - {reservation.owner}\n'
            f'Столик №{reservation.table}\n'
            f'Комментарий: {reservation.comment}\n'
        )

    else:
        subject = body = None

    return subject, body


def send_reservation_notification(reservation, action, user=None, request=None):
    if user and user.pk != reservation.owner.pk:
        return

    subject, body = build_reservation_mail(reservation, action, request=request)
    if subject and body:
        send_reservation_email.delay(subject, body)


def round_time_to_next_slot(dt):
    minute = dt.minute
    if minute == 0:
        return dt.replace(minute=30, second=0, microsecond=0)
    elif minute <= 30:
        return dt.replace(minute=30, second=0, microsecond=0)
    else:
        dt = dt.replace(minute=0, second=0, microsecond=0)
        return dt + timedelta(hours=1)
