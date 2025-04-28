import smtplib
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from config.settings import CACHE_ENABLED, EMAIL_HOST_USER
from mailing.models import Attempt, Mailing


class MailingService:

    @staticmethod
    def send(request, pk):
        mailing = Mailing.objects.get(pk=pk)
        subject = mailing.message.theme
        message = mailing.message.content
        recipients = [
            recipient.email for recipient in mailing.recipients.all()]

        start = timezone.now()

        try:
            response = send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                recipients,
                fail_silently=False)

        except smtplib.SMTPException as e:
            MailingService.create_attempt(
                status='failure', response=e, mailing=mailing)

        else:
            end = timezone.now()
            MailingService.create_attempt(
                status='success', response=response, mailing=mailing)
            MailingService.update_status(
                mailing=mailing, start=start, end=end)

        finally:
            return redirect(reverse('mailing:mailing_list'))

    @staticmethod
    def create_attempt(status, response, mailing):
        attempt = Attempt.objects.create(
            status=status, response=response, mailing=mailing)
        attempt.save()

    @staticmethod
    def update_status(mailing, start, end):
        mailing.start = timezone.localtime(start)
        mailing.end = timezone.localtime(end)
        mailing.status = 'completed'
        mailing.save()

    @staticmethod
    def caching(queryset, model):
        if not CACHE_ENABLED:
            return queryset
        key = str(model) + '_list'
        objects = cache.get(key)
        if objects is not None:
            return objects
        objects = queryset
        cache.set(key, objects, 60 * 1)
        return objects
