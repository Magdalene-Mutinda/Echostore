from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Review
from django import forms
from .models import Review

from .models import Address, Region, City

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['additional_phone', 'address', 'additional_info', 'region', 'city']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'e.g. House number, Street, Estate'}),
            'additional_info': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'e.g. Landmark, instructions (optional)'}),
            'additional_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Additional phone (optional)'}),
            'region': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)

    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'cols': 60,
            'class': 'form-control',
            'placeholder': 'Write your review here...'
        })
    )

    class Meta:
        model = Review
        fields = ['rating', 'comment']



class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )

    email = forms.EmailField(
        label="Email (optional)",
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        label="Phone (optional)",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'})
    )


class CustomSignupForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    phone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'})
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

from django import forms
from django.core.exceptions import ValidationError

def validate_excel_file(file):
    valid_extensions = ['xls', 'xlsx']
    ext = file.name.split('.')[-1].lower()
    if ext not in valid_extensions:
        raise ValidationError("Only Excel files (.xls or .xlsx) are allowed.")

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label="Select Excel File",
        validators=[validate_excel_file]
    )
