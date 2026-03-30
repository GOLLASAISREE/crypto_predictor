from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, date
import json

from .models import UserProfile, PredictionResult, Cryptocurrency, ContactMessage
from .forms import UserRegistrationForm, PredictionForm, ContactForm, UserEditForm
from .ml_engine import run_prediction

CRYPTO_INFO = {
    'BTC': {'name': 'Bitcoin', 'color': '#F7931A', 'icon': '₿'},
    'ETH': {'name': 'Ethereum', 'color': '#627EEA', 'icon': 'Ξ'},
    'BNB': {'name': 'Binance Coin', 'color': '#F3BA2F', 'icon': 'BNB'},
    'ADA': {'name': 'Cardano', 'color': '#0033AD', 'icon': 'ADA'},
    'SOL': {'name': 'Solana', 'color': '#9945FF', 'icon': 'SOL'},
    'XRP': {'name': 'XRP', 'color': '#00AAE4', 'icon': 'XRP'},
    'DOGE': {'name': 'Dogecoin', 'color': '#C3A634', 'icon': 'Ð'},
    'DOT': {'name': 'Polkadot', 'color': '#E6007A', 'icon': 'DOT'},
    'MATIC': {'name': 'Polygon', 'color': '#8247E5', 'icon': 'MATIC'},
    'LTC': {'name': 'Litecoin', 'color': '#BFBBBB', 'icon': 'Ł'},
}


def home(request):
    return render(request, 'crypto_app/home.html', {'crypto_info': CRYPTO_INFO})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'crypto_app/login.html')


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and (user.is_staff or hasattr(user, 'userprofile') and user.userprofile.role == 'admin'):
            login(request, user)
            messages.success(request, f'Admin login successful. Welcome, {user.username}!')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials.')
    return render(request, 'crypto_app/admin_login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'crypto_app/register.html', {'form': form})


@login_required
def dashboard(request):
    recent_predictions = PredictionResult.objects.filter(user=request.user).order_by('-created_at')[:5]
    form = PredictionForm()
    return render(request, 'crypto_app/dashboard.html', {
        'form': form,
        'recent_predictions': recent_predictions,
        'crypto_info': CRYPTO_INFO,
    })


@login_required
def predict(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST)
        if form.is_valid():
            crypto_symbol = form.cleaned_data['crypto']
            algorithm = form.cleaned_data['algorithm']
            target_date = form.cleaned_data['target_date']

            try:
                result = run_prediction(crypto_symbol, algorithm, target_date)

                algo_display = dict(PredictionForm.ALGORITHM_CHOICES).get(algorithm, algorithm)
                crypto_obj, _ = Cryptocurrency.objects.get_or_create(
                    symbol=crypto_symbol,
                    defaults={'name': CRYPTO_INFO.get(crypto_symbol, {}).get('name', crypto_symbol)}
                )

                pred_record = PredictionResult.objects.create(
                    user=request.user,
                    crypto=crypto_obj,
                    algorithm=algorithm,
                    prediction_date=target_date,
                    predicted_price=result['predicted_price'],
                    current_price=result['current_price'],
                    accuracy=result.get('accuracy'),
                    mae=result.get('mae'),
                    rmse=result.get('rmse'),
                    r2_score=result.get('r2_score'),
                    investment_suggestion=result.get('investment_suggestion', '')
                )

                return render(request, 'crypto_app/prediction_result.html', {
                    'result': result,
                    'crypto_symbol': crypto_symbol,
                    'crypto_info': CRYPTO_INFO.get(crypto_symbol, {}),
                    'algorithm': algo_display,
                    'target_date': target_date,
                    'prediction_id': pred_record.id,
                })
            except Exception as e:
                messages.error(request, f'Prediction error: {str(e)}')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid form data.')
    return redirect('dashboard')


@login_required
def prediction_history(request):
    predictions = PredictionResult.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'crypto_app/prediction_history.html', {
        'predictions': predictions,
        'crypto_info': CRYPTO_INFO
    })


# ─── ADMIN VIEWS ────────────────────────────────────────────────────────────────

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('admin_login')
        if not (request.user.is_staff or
                (hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin')):
            messages.error(request, 'Admin access required.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_predictions = PredictionResult.objects.count()
    recent_predictions = PredictionResult.objects.order_by('-created_at')[:10]
    users = User.objects.filter(is_staff=False).order_by('-date_joined')[:10]
    return render(request, 'crypto_app/admin_dashboard.html', {
        'total_users': total_users,
        'total_predictions': total_predictions,
        'recent_predictions': recent_predictions,
        'users': users,
    })


@admin_required
def manage_users(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'crypto_app/manage_users.html', {'users': users})


@admin_required
def edit_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {target_user.username} updated.')
            return redirect('manage_users')
    else:
        form = UserEditForm(instance=target_user)
    return render(request, 'crypto_app/edit_user.html', {'form': form, 'target_user': target_user})


@admin_required
def delete_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        username = target_user.username
        target_user.delete()
        messages.success(request, f'User {username} deleted.')
    return redirect('manage_users')


@admin_required
def toggle_user(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_user.is_active = not target_user.is_active
    target_user.save()
    status = 'activated' if target_user.is_active else 'deactivated'
    messages.success(request, f'User {target_user.username} {status}.')
    return redirect('manage_users')


@admin_required
def admin_predictions(request):
    predictions = PredictionResult.objects.all().order_by('-created_at')
    return render(request, 'crypto_app/admin_predictions.html', {
        'predictions': predictions, 'crypto_info': CRYPTO_INFO
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            if request.user.is_authenticated:
                msg.user = request.user
            msg.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, 'crypto_app/contact.html', {'form': form})
