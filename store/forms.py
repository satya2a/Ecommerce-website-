from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30)
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}))
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
