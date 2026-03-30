import os

import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crypto_predictor.settings')


def ensure_vercel_bootstrap():
	if not os.getenv('VERCEL'):
		return

	try:
		django.setup()
		call_command('migrate', interactive=False, run_syncdb=True, verbosity=0)

		from django.contrib.auth.models import User
		from crypto_app.models import Cryptocurrency, UserProfile

		if not User.objects.filter(username='admin').exists():
			admin = User.objects.create_superuser(
				username='admin',
				email='admin@cryptopredictor.com',
				password='admin123',
				first_name='Admin',
				last_name='User',
			)
			UserProfile.objects.get_or_create(user=admin, defaults={'role': 'admin'})

		if not User.objects.filter(username='demo').exists():
			demo = User.objects.create_user(
				username='demo',
				email='demo@cryptopredictor.com',
				password='demo123',
				first_name='Demo',
				last_name='User',
			)
			UserProfile.objects.get_or_create(user=demo, defaults={'role': 'user'})

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
	except Exception as exc:
		# Keep app booting even if bootstrap fails; error details stay in logs.
		print(f'Vercel bootstrap warning: {exc}')


ensure_vercel_bootstrap()
application = get_wsgi_application()
