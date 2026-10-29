from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Student, Course, Result

User = get_user_model()


class StudentRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    phone = forms.CharField(max_length=30, required=False)
    address = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "address",
            "courses",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["courses"].queryset = Course.objects.filter(
            is_active=True
        )

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
        return user


class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username or student number"
    )


class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["score"]