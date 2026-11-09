
from decimal import Decimal

from django.db.models import DecimalField, F, Sum

from .models import Sale, Expense


def calculate_finances(event=None):
    """
    Calculate revenue, expenses, and estimated profit.

    When event is None, use records from the entire business.
    Otherwise, calculate totals only for the selected event.
    """
    sales = Sale.objects.all()
    expenses = Expense.objects.all()

    if event is not None:
        sales = sales.filter(event=event)
        expenses = expenses.filter(event=event)

    revenue = sales.aggregate(
        total=Sum(
            F("quantity") * F("unit_price"),
            output_field=DecimalField(
                max_digits=18,
                decimal_places=2
            )
        )
    )["total"] or Decimal("0.00")

    total_expenses = expenses.aggregate(
        total=Sum("amount")
    )["total"] or Decimal("0.00")

    profit = revenue - total_expenses

    return {
        "revenue": revenue,
        "expenses": total_expenses,
        "profit": profit,
    }
