import secrets
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetDoneView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from config.settings import EMAIL_HOST_USER
from users.forms import UserCreationForm, UserUpdateForm
from users.models import User


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.blocked = True
        user.token = secrets.token_hex(16)
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{user.token}/'
        send_mail(subject='Подтверждение почты',
                  message=f'Перейдите по ссылке, чтобы подтвердить почту:'
                          f'{url}',
                  from_email=EMAIL_HOST_USER, recipient_list=[user.email])
        return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    user.blocked = False
    user.save()
    return redirect(reverse('users:login'))


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy('users:user_detail')

    @staticmethod
    def block_user(request, pk):
        block_user = User.objects.get(pk=pk)
        if not request.user.has_per('users.can_block_user'):
            raise PermissionDenied
        else:
            block_user.blocked = True
            block_user.save()
        return redirect(reverse('mailing:main'))


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User


class UserListView(LoginRequiredMixin, ListView):
    model = User


class MyPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html',
    success_url = reverse_lazy('users:password_reset_confirm')
