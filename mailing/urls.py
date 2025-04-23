from django.urls import path
from mailing.apps import MailingConfig
from mailing.services import MailingService
from mailing.views import (
    MailingCreateView, MailingDeleteView,
    MailingListView, MailingUpdateView, MessageCreateView, MessageDeleteView,
    MessageDetailView, MessageListView, MessageUpdateView, RecipientCreateView,
    RecipientDeleteView, RecipientDetailView, RecipientListView,
    RecipientUpdateView, StatisticsView, main_view, MailingDetailView)

app_name = MailingConfig.name

urlpatterns = [
    path('', main_view, name='main'),
    path('recipient/create/',
         RecipientCreateView.as_view(), name='recipient_create'),
    path('recipient/list/',
         RecipientListView.as_view(), name='recipient_list'),
    path('recipient/<int:pk>/',
         RecipientDetailView.as_view(), name='recipient_detail'),
    path('recipient/<int:pk>/update/',
         RecipientUpdateView.as_view(), name='recipient_update'),
    path('recipient/<int:pk>/delete/',
         RecipientDeleteView.as_view(), name='recipient_confirm_delete'),
    path('message/create/',
         MessageCreateView.as_view(), name='message_create'),
    path('message/list/',
         MessageListView.as_view(), name='message_list'),
    path('message/<int:pk>/',
         MessageDetailView.as_view(), name='message_detail'),
    path('message/<int:pk>/update/',
         MessageUpdateView.as_view(), name='message_update'),
    path('message/<int:pk>/delete/',
         MessageDeleteView.as_view(), name='message_confirm_delete'),
    path('mailing/list/',
         MailingListView.as_view(), name='mailing_list'),
    path('mailing/statistics/',
         StatisticsView.as_view(), name='statistics'),
    path('mailing/<int:pk>/stop/',
         MailingUpdateView.stop_mailing, name='stop_mailing'),
    path('mailing/update/<int:pk>',
         MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing/create/',
         MailingCreateView.as_view(), name='mailing_create'),
    path('mailing/<int:pk>/send/',
         MailingService.send, name='send'),
    path('mailing/<int:pk>/delete/',
         MailingDeleteView.as_view(), name='mailing_confirm_delete'),
    path('mailing/<int:pk>/',
         MailingDetailView.as_view(), name='mailing_detail'),
]
