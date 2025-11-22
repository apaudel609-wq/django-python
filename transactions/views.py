from django.shortcuts import render, redirect
from .forms import TransactionForm
from datetime import date
from django.views.generic import TemplateView
from .services.financial import calculate_net_balance

from django.contrib.auth.decorators import login_required

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.user, request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(request.user)

    return render(request, "transactions/add_transaction.html", {"form": form})
# ================================
# W1.4 Basic CRUD Views
# Implement ListView and CreateView for Transactions
# ================================

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm

from django.contrib.auth.mixins import LoginRequiredMixin

class TransactionListView(LoginRequiredMixin, ListView):
 
    model = Transaction
    template_name = "transactions/transaction_list.html"
    context_object_name = "transactions"
    ordering = ["-date"]  # newest first

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by("-date")


class TransactionCreateView(LoginRequiredMixin, CreateView):
    
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/add_transaction.html"
    success_url = reverse_lazy("transaction_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TransactionDetailView(LoginRequiredMixin, DetailView):
    model = Transaction
    template_name = "transactions/transaction_detail.html"
    context_object_name = "transaction"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transactions/add_transaction.html" # Reuse form template
    success_url = reverse_lazy("transaction_list")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    template_name = "transactions/transaction_confirm_delete.html"
    success_url = reverse_lazy("transaction_list")

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = "transactions/category_list.html"
    context_object_name = "categories"

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "transactions/add_category.html"
    success_url = reverse_lazy("transaction_list") # Redirect to transaction list for now

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "transactions/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get user's transactions
        user_transactions = Transaction.objects.filter(user=self.request.user).order_by("-date")

        # 1. Calculate MTD Net Balance
        # Optimized Service Function (W4.3)
        from .services.financial import calculate_mtd_balance
        context['net_balance'] = calculate_mtd_balance(self.request.user)

        # 2. Get Recent 10 Transactions
        context['recent_transactions'] = user_transactions[:10]

        return context

