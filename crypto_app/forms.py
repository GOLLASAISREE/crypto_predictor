from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, PredictionResult, ContactMessage


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone=self.cleaned_data.get('phone', ''),
                role='user'
            )
        return user


class PredictionForm(forms.Form):
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin (BTC)'),
        ('ETH', 'Ethereum (ETH)'),
        ('BNB', 'Binance Coin (BNB)'),
        ('ADA', 'Cardano (ADA)'),
        ('SOL', 'Solana (SOL)'),
        ('XRP', 'XRP (XRP)'),
        ('DOGE', 'Dogecoin (DOGE)'),
        ('DOT', 'Polkadot (DOT)'),
        ('MATIC', 'Polygon (MATIC)'),
        ('LTC', 'Litecoin (LTC)'),
    ]
    ALGORITHM_CHOICES = [
        ('lr', 'Linear Regression'),
        ('lstm', 'LSTM (Long Short-Term Memory)'),
        ('svm', 'Support Vector Machine'),
        ('rf', 'Random Forest'),
    ]

    crypto = forms.ChoiceField(choices=CRYPTO_CHOICES, label='Cryptocurrency')
    algorithm = forms.ChoiceField(choices=ALGORITHM_CHOICES, label='ML Algorithm')
    target_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Prediction Date')


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active']
