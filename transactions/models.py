from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('name', 'user')   # ⬅ ensures unique category names per user
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")

    # CRITICAL FINTECH STANDARD: Use DecimalField for currency
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    date = models.DateField()

    note = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.category})"
