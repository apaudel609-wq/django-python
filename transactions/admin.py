from django.contrib import admin
from .models import Category, Transaction  # <-- import your models

# Register your models here.

admin.site.register(Category)
admin.site.register(Transaction)
