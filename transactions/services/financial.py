from decimal import Decimal

def calculate_net_balance(transactions):
    """
    Calculates the net balance from a list of transactions.
    
    Args:
        transactions: A list (or iterable) of Transaction objects.
                      Each object must have 'amount' (Decimal) and 'transaction_type' (str).
                      
    Returns:
        Decimal: The total net balance (Income - Expenses).
    """
    balance = Decimal('0.00')
    
    for transaction in transactions:
        if transaction.transaction_type == 'INCOME':
            balance += transaction.amount
        elif transaction.transaction_type == 'EXPENSE':
            balance -= transaction.amount
            
    return balance


from datetime import date
from django.db.models import Sum, Case, When, DecimalField, F
from transactions.models import Transaction

def calculate_mtd_balance(user):
    """
    Calculates the Month-to-Date (MTD) Net Balance for a user using ORM aggregation.
    
    Args:
        user: The user object.
        
    Returns:
        Decimal: The net balance (Income - Expenses) for the current month.
    """
    today = date.today()
    
    # Filter for current month and user
    mtd_transactions = Transaction.objects.filter(
        user=user,
        date__year=today.year,
        date__month=today.month
    )
    
    # Aggregate: Sum(Income) - Sum(Expense)
    # We use Case/When to treat Expenses as negative values
    aggregation = mtd_transactions.aggregate(
        net_balance=Sum(
            Case(
                When(transaction_type='INCOME', then='amount'),
                When(transaction_type='EXPENSE', then=-1 * F('amount')), # We need F() expression here? No, simpler to just sum signed values if we could.
                                                                         # Actually, let's stick to the plan: Sum(Case(...))
                default=0,
                output_field=DecimalField()
            )
        )
    )
    
    # Return the result, defaulting to 0 if None (no transactions)
    return aggregation['net_balance'] or Decimal('0.00')

