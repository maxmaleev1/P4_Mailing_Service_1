from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)

from mailing.forms import MailingForm, MessageForm, RecipientForm
from mailing.models import Attempt, Mailing, Message, Recipient
from mailing.services import MailingService


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    form_class = RecipientForm
    success_url = reverse_lazy('mailing:recipient_detail')

    def form_valid(self, form):
        recipient = form.save()
        user = self.request.user
        recipient.owner = user
        recipient.save()
        return super().form_valid(form)


class RecipientDetailView(LoginRequiredMixin, DetailView):
    model = Recipient

    def get_queryset(self):
        if self.request.user.user.has_perm('can_view_recipient'):
            return MailingService.caching(super().get_queryset(
                Recipient.objects.all()))
        else:
            return MailingService.caching(super().get_queryset(
                Recipient.objects.filter(owner=self.request.user)))


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient

    def get_queryset(self):
        if self.request.user.user.has_perm('can_view_recipient'):
            return MailingService.caching(super().get_queryset(
                Recipient.objects.all()))
        else:
            return MailingService.caching(super().get_queryset(
                Recipient.objects.filter(owner=self.request.user)))


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    form_class = RecipientForm

    def get_success_url(self):
        return reverse_lazy(
            'mailing:recipient_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return RecipientForm
        raise PermissionDenied


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    success_url = reverse_lazy('mailing:recipient_list')


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailing:message_detail')

    def form_valid(self, form):
        message = form.save()
        user = self.request.user
        message.owner = user
        message.save()
        return super().form_valid(form)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message

    def get_queryset(self):
        if self.request.user.user.has_perm('can_view_message'):
            return MailingService.caching(super().get_queryset(
                Message.objects.all()))
        else:
            return MailingService.caching(super().get_queryset(
                Message.objects.filter(owner=self.request.user)))


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self):
        if self.request.user.user.has_perm('can_view_message'):
            return MailingService.caching(super().get_queryset(
                Message.objects.all()))
        else:
            return MailingService.caching(super().get_queryset(
                Message.objects.filter(owner=self.request.user)))


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def get_success_url(self):
        return reverse_lazy(
            'mailing:message_detail', kwargs={'pk': self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailing:message_list')


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailing:mailing_list')

    def form_valid(self, form):
        mailing = form.save()
        user = self.request.user
        mailing.owner = user
        mailing.save()
        return super().form_valid(form)


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_queryset(self):
        return MailingService.caching(super().get_queryset(
                Mailing.objects.filter(owner=self.request.user)))


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_queryset(self):
        return MailingService.caching(super().get_queryset(
                Mailing.objects.filter(owner=self.request.user)))


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm

    def get_success_url(self):
        return reverse_lazy(
            'mailing:mailing_detail', kwargs={'pk': self.object.pk})

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailingForm
        raise PermissionDenied

    @staticmethod
    def stop_mailing(request, pk):
        stopped_mailing = Mailing.objects.get(pk=pk)
        if not request.user.has_perm('mailing.can_stop_mailing'):
            raise PermissionDenied
        else:
            stopped_mailing.status = 'completed'
            stopped_mailing.save()
        return redirect(reverse('mailing:mailing_detail'))


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:mailing_list')

    def get_form_class(self):
        user = self.request.user
        if self.object.owner == user:
            return MailingForm
        if user.has_perms(['mailing.can_delete_mailing']):
            return MailingForm
        raise PermissionDenied


class StatisticsView(TemplateView):
    template_name = 'mailing/statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        mailings = Mailing.objects.filter(owner=user)
        attempts = Attempt.objects.filter(mailing__in=mailings)

        successful = 0
        failed = 0
        mailing_count = 0

        for attempt in attempts:
            if attempt.status == 'success':
                successful += 1
                mailing_count += attempt.mailing.recipients.count()
            if attempt.status == 'failure':
                failed += 1

        context['successful'] = successful
        context['failed'] = failed
        context['mailing_count'] = mailing_count
        context['attempts'] = attempts.count()
        return context


def main_view(request):
    mailings = Mailing.objects.count()
    launched_mailings = Mailing.objects.filter(status='launched').count()
    recipients = Recipient.objects.count()

    context = {
        'mailings': mailings,
        'launched_mailing': launched_mailings,
        'recipients': recipients}

    return render(request, 'mailing/main.html', context)
