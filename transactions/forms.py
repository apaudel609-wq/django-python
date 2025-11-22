from django import forms
from .models import Transaction, Category
from datetime import date


class TransactionForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = self.fields['category'].queryset.filter(user=user)

    class Meta:
        model = Transaction
        fields = ['category', 'amount', 'transaction_type', 'date', 'note']

    def clean_amount(self):
        """
        Validate that amount is greater than 0.
        """
        amount = self.cleaned_data.get('amount')

        if amount is None or amount <= 0:
            raise forms.ValidationError("Amount must be greater than $0.")

        return amount

    def clean_date(self):
        """
        Prevent selecting a future date.
        """
        transaction_date = self.cleaned_data.get('date')

        if transaction_date and transaction_date > date.today():
            raise forms.ValidationError("Transaction date cannot be in the future.")

        return transaction_date


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

