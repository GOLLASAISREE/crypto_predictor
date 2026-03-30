from django.contrib import admin
from .models import UserProfile, Cryptocurrency, PriceHistory, PredictionResult, ContactMessage

admin.site.register(UserProfile)
admin.site.register(Cryptocurrency)
admin.site.register(PriceHistory)
admin.site.register(PredictionResult)
admin.site.register(ContactMessage)

admin.site.site_header = "CryptoPredictor Admin"
admin.site.site_title = "CryptoPredictor"
admin.site.index_title = "Admin Panel"
