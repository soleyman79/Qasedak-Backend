from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')

    def is_valid(self) -> bool:
        valid = super().is_valid()
        if User.objects.filter(Q(username=f'user-{self.cleaned_data["email"]}') | Q(username=f'user-{self.cleaned_data["phone"]}')):
            return False
        return valid

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user
