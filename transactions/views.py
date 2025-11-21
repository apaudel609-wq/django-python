from django.shortcuts import render, redirect
from .forms import TransactionForm

def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TransactionForm()

    return render(request, "transactions/add_transaction.html", {"form": form})
# ================================
# W1.4 Basic CRUD Views
# Implement ListView and CreateView for Transactions
# ================================

from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Transaction
from .forms import TransactionForm

class TransactionListView(ListView):
 
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"
    ordering = ["-date"]  # newest first


class TransactionCreateView(CreateView):
    
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/add_transaction.html"
    success_url = reverse_lazy("transaction_list")
