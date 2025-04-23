from django.db import models
from users.models import User


class Recipient(models.Model):
    email = models.CharField(max_length=30, unique=True, verbose_name='Email')
    name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий')
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'получатель'
        verbose_name_plural = 'получатели'
        permissions = [('can_view_recipient', 'Can view recipient'),]

    def __str__(self):
        return self.email


class Message(models.Model):
    theme = models.CharField(max_length=50, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')
    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'
        permissions = [('can_view_message', 'Can view message'),]

    def __str__(self):
        return self.theme


class Mailing(models.Model):
    COMPLETED = 'completed'
    CREATED = 'created'
    LAUNCHED = 'launched'

    STATUS_CHOICES = [
        (CREATED, 'Создана'), (COMPLETED, 'Завершена'), (LAUNCHED, 'Запущена'),
    ]

    start = models.DateTimeField(
        verbose_name='Первая отправка', null=True, blank=True)

    end = models.DateTimeField(
        verbose_name='Окончание отправки', null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')

    message = models.ForeignKey(
        'Message',
        on_delete=models.CASCADE,
        verbose_name='Сообщение',
        related_name='mailings')

    recipients = models.ManyToManyField(
        'Recipient', verbose_name='Получатели рассылки')

    owner = models.ForeignKey(
        User,
        verbose_name='Владелец',
        on_delete=models.CASCADE,
        related_name='mailing',
        blank=True, null=True)

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'
        ordering = ['message', 'owner']
        permissions = [('can_stop_mailing', 'Can stop mailing'),]

    def __str__(self):
        return f'Рассылка + {self.message}'


class Attempt(models.Model):
    SUCCESS = 'success'
    FAILURE = 'failure'

    STATUS_CHOICES = [(SUCCESS, 'Успешно'), (FAILURE, 'Неуспешно'),]

    datetime = models.DateTimeField(verbose_name='Время попытки')

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')

    response = models.TextField(verbose_name='Ответ почтового сервера')

    mailing = models.ForeignKey(
        'Mailing',
        on_delete=models.CASCADE,
        verbose_name='Рассылка',
        related_name='attempt')

    class Meta:
        verbose_name = 'попытка рассылки'
        verbose_name_plural = 'попытки рассылки'
