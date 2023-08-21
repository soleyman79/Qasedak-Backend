from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'phone', 'password1', 'password2')

    def is_valid(self):
        if not super().is_valid():
            errorMessage = ''
            for message in list(super().errors.values()):
                errorMessage += message[0] + '\n'
            print(errorMessage)
            return errorMessage
        try:
            if User.objects.filter(Q(username=f'user-{self.cleaned_data["email"]}') | Q(username=f'user-{self.cleaned_data["phone"]}')):
                return 'Duplicate Username'
            return 'OK'
        except:
            pass

    def save(self, commit=True):
        user = super().save(commit=commit)
        return user
