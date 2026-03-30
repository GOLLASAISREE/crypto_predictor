from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [('admin', 'Admin'), ('user', 'User')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone = models.CharField(max_length=15, blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class Cryptocurrency(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    logo_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"


class PriceHistory(models.Model):
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    date = models.DateField()
    open_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    close_price = models.FloatField()
    volume = models.FloatField()

    class Meta:
        unique_together = ('crypto', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.crypto.symbol} - {self.date}"


class PredictionResult(models.Model):
    ALGORITHM_CHOICES = [
        ('lr', 'Linear Regression'),
        ('lstm', 'LSTM'),
        ('svm', 'Support Vector Machine'),
        ('rf', 'Random Forest'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=10, choices=ALGORITHM_CHOICES)
    prediction_date = models.DateField()
    predicted_price = models.FloatField()
    current_price = models.FloatField(null=True, blank=True)
    accuracy = models.FloatField(null=True, blank=True)
    mae = models.FloatField(null=True, blank=True)
    rmse = models.FloatField(null=True, blank=True)
    r2_score = models.FloatField(null=True, blank=True)
    investment_suggestion = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.crypto.symbol} - {self.algorithm} - {self.prediction_date}"


class ContactMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"
