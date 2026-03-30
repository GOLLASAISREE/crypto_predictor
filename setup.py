"""
Auto-setup script: Creates DB, migrations, admin user, and sample data.
Run once: python setup.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_predictor.settings')

# Run migrations first
os.system(f'{sys.executable} manage.py makemigrations')
os.system(f'{sys.executable} manage.py makemigrations crypto_app')
os.system(f'{sys.executable} manage.py migrate')

django.setup()

from django.contrib.auth.models import User
from crypto_app.models import UserProfile, Cryptocurrency

# ── Create Admin ─────────────────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@cryptopredictor.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})
    print("✅ Admin created  →  username: admin  |  password: admin123")
else:
    print("ℹ️  Admin already exists")

# ── Create Demo User ──────────────────────────────────────────────────────────
if not User.objects.filter(username='demo').exists():
    demo = User.objects.create_user(
        username='demo',
        email='demo@cryptopredictor.com',
        password='demo123',
        first_name='Demo',
        last_name='User'
    )
    UserProfile.objects.get_or_create(user=demo, defaults={'role': 'user'})
    print("✅ Demo user created  →  username: demo  |  password: demo123")
else:
    print("ℹ️  Demo user already exists")

# ── Seed Cryptocurrencies ─────────────────────────────────────────────────────
cryptos = [
    ('BTC', 'Bitcoin'),
    ('ETH', 'Ethereum'),
    ('BNB', 'Binance Coin'),
    ('ADA', 'Cardano'),
    ('SOL', 'Solana'),
    ('XRP', 'XRP'),
    ('DOGE', 'Dogecoin'),
    ('DOT', 'Polkadot'),
    ('MATIC', 'Polygon'),
    ('LTC', 'Litecoin'),
]
for sym, name in cryptos:
    Cryptocurrency.objects.get_or_create(symbol=sym, defaults={'name': name})
print(f"✅ Seeded {len(cryptos)} cryptocurrencies")

print("\n" + "="*50)
print("🚀 SETUP COMPLETE!")
print("="*50)
print("Run the server:  python manage.py runserver")
print("Open browser:    http://127.0.0.1:8000/")
print()
print("LOGIN CREDENTIALS:")
print("  Admin  →  username: admin  |  password: admin123")
print("  User   →  username: demo   |  password: demo123")
print("="*50)
