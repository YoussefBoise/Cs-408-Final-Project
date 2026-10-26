from django import forms
from .models import MenuItem, InventoryItem


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem

        fields = [
            "name",
            "category",
            "description",
            "price",
            "available",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "category": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 3}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "available": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_price(self):
        price = self.cleaned_data["price"]

        if price < 0:
            raise forms.ValidationError(
                "Price cannot be negative."
            )

        return price


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem

        fields = [
            "name",
            "category",
            "quantity",
            "unit",
            "cost",
            "low_stock_amount",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "category": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "quantity": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "unit": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "cost": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
            "low_stock_amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01"}
            ),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data["quantity"]

        if quantity < 0:
            raise forms.ValidationError(
                "Quantity cannot be negative."
            )

        return quantity

    def clean_cost(self):
        cost = self.cleaned_data["cost"]

        if cost < 0:
            raise forms.ValidationError(
                "Cost cannot be negative."
            )

        return cost

    def clean_low_stock_amount(self):
        amount = self.cleaned_data["low_stock_amount"]

        if amount < 0:
            raise forms.ValidationError(
                "Low-stock threshold cannot be negative."
            )

        return amount