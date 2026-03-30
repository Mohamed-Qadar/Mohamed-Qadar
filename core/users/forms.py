"""
Forms for user authentication and registration.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, UserProfile


class CitizenRegistrationForm(UserCreationForm):
    """Form for citizen registration."""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    location = forms.CharField(max_length=200, required=True)
    national_id = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone',
                  'location', 'national_id', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'citizen'
        if commit:
            user.save()
        return user


class GovernmentRegistrationForm(UserCreationForm):
    """Form for government official registration."""
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    institution = forms.ModelChoiceField(
        queryset=None,
        required=True,
        empty_label="Select Institution"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone',
                  'institution', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from institutions.models import Institution
        self.fields['institution'].queryset = Institution.objects.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'government'
        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""
    class Meta:
        model = UserProfile
        fields = ['bio', 'date_of_birth', 'address', 'city', 'state',
                  'postal_code', 'email_notifications', 'sms_notifications']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }


class UserUpdateForm(forms.ModelForm):
    """Form for updating user basic information."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'location', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(),
        }
