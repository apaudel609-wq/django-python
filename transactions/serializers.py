from rest_framework import serializers
from .models import Transaction, Category
from datetime import date

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TransactionSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Transaction
        fields = ['id', 'category', 'category_name', 'amount', 'transaction_type', 'date', 'note', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_amount(self, value):
        """
        Check that the amount is positive.
        """
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0.")
        return value

    def validate_date(self, value):
        """
        Check that the date is not in the future.
        """
        if value > date.today():
            raise serializers.ValidationError("Transaction date cannot be in the future.")
        return value
