from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from config.settings import EMAIL_HOST_USER
from mailing.models import Mailing, Message


class Command(BaseCommand):
    help = 'Выполняет рассылку через консоль'

    def handle(self, *args, **kwargs):
        messages = Mailing.objects.filter(
            Q(status='created'), Q(start__gt=timezone.now().date()))

        for message in messages:

            send_mail(
                subject=Message.theme,
                message=Message.body,
                from_email=EMAIL_HOST_USER,
                recipient_list=[Mailing.recipients])

            message.is_sent = True
            message.save()
            self.stdout.write(
                self.style.SUCCESS(f'Отправлено: {message.theme}'))
