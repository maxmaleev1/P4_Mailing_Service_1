from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from users.models import User  # Используем кастомную модель


class Command(BaseCommand):
    help = 'Заполняет группу "Менеджеры" пользователями'

    def add_arguments(self, parser):
        # Оставляем только emails
        parser.add_argument('emails', nargs='+', type=str,
                            help='Email пользователей')

    def handle(self, *args, **kwargs):
        emails = kwargs['emails']
        group_name = "Менеджеры"  # Фиксированное название

        group, created = Group.objects.get_or_create(name=group_name)

        for email in emails:
            user, created = User.objects.get_or_create(
                email=email,
                defaults={'username': email.split('@')[0]}
            )
            user.groups.add(group)
            self.stdout.write(
                f'Пользователь {email} добавлен в группу {group_name}')
