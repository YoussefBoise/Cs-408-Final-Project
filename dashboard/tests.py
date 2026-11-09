from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import MenuItem, InventoryItem, Event, Sale, Expense


class PageTests(TestCase):

    def test_homepage_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Food Trailer Management")
        self.assertContains(response, "Dashboard")


class ModelTests(TestCase):

    def test_menu_item(self):
        item = MenuItem.objects.create(
            name="Corn Dog",
            category="Food",
            price=Decimal("5.00")
        )
        self.assertEqual(item.name, "Corn Dog")

    def test_inventory_item(self):
        item = InventoryItem.objects.create(
            name="Flour",
            category="Ingredients",
            quantity=Decimal("10.00"),
            unit="lbs",
            cost=Decimal("2.50"),
            low_stock_amount=Decimal("3.00")
        )
        self.assertEqual(item.quantity, Decimal("10.00"))

    def test_event(self):
        event = Event.objects.create(
            name="Food Festival",
            location="Boise",
            event_date=date(2026, 11, 10),
            application_deadline=date(2026, 11, 1),
            application_fee=Decimal("50.00")
        )
        self.assertEqual(event.application_status, "Not Applied")

    def test_sale(self):
        item = MenuItem.objects.create(
            name="Corn Dog",
            category="Food",
            price=Decimal("5.00")
        )
        sale = Sale.objects.create(
            menu_item=item,
            quantity=2,
            unit_price=Decimal("5.00"),
            sale_date=date(2026, 10, 18)
        )
        self.assertEqual(sale.quantity, 2)

    def test_expense(self):
        expense = Expense.objects.create(
            description="Propane",
            category="Supplies",
            amount=Decimal("30.00"),
            date=date(2026, 10, 18)
        )
        self.assertEqual(expense.amount, Decimal("30.00"))


class MenuManagementTests(TestCase):

    def setUp(self):
        self.item = MenuItem.objects.create(
            name="Corn Dog",
            category="Food",
            description="Classic corn dog",
            price=Decimal("6.00"),
            available=True
        )

    def test_menu_page_loads(self):
        response = self.client.get(reverse("menu_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Corn Dog")

    def test_menu_detail_page(self):
        response = self.client.get(
            reverse("menu_detail", args=[self.item.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Classic corn dog")

    def test_create_menu_item(self):
        response = self.client.post(
            reverse("menu_create"),
            {
                "name": "Funnel Cake",
                "category": "Dessert",
                "description": "Powdered sugar",
                "price": "8.00",
                "available": "on"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            MenuItem.objects.filter(name="Funnel Cake").exists()
        )

    def test_edit_menu_item(self):
        response = self.client.post(
            reverse("menu_edit", args=[self.item.pk]),
            {
                "name": "Large Corn Dog",
                "category": "Food",
                "description": "Updated item",
                "price": "7.50",
                "available": "on"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Large Corn Dog")
        self.assertEqual(self.item.price, Decimal("7.50"))

    def test_delete_menu_item(self):
        response = self.client.post(
            reverse("menu_delete", args=[self.item.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            MenuItem.objects.filter(pk=self.item.pk).exists()
        )

    def test_delete_requires_confirmation(self):
        self.client.get(
            reverse("menu_delete", args=[self.item.pk])
        )

        self.assertTrue(
            MenuItem.objects.filter(pk=self.item.pk).exists()
        )

    def test_negative_price_rejected(self):
        response = self.client.post(
            reverse("menu_create"),
            {
                "name": "Invalid Item",
                "category": "Food",
                "description": "Test",
                "price": "-5.00",
                "available": "on"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Price cannot be negative.")
        self.assertFalse(
            MenuItem.objects.filter(name="Invalid Item").exists()
        )


class InventoryManagementTests(TestCase):

    def setUp(self):
        self.item = InventoryItem.objects.create(
            name="Flour",
            category="Ingredients",
            quantity=Decimal("5.00"),
            unit="lbs",
            cost=Decimal("12.00"),
            low_stock_amount=Decimal("10.00")
        )

    def test_inventory_page_loads(self):
        response = self.client.get(reverse("inventory_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flour")

    def test_create_inventory_item(self):
        response = self.client.post(
            reverse("inventory_create"),
            {
                "name": "Cooking Oil",
                "category": "Ingredients",
                "quantity": "20.00",
                "unit": "gallons",
                "cost": "30.00",
                "low_stock_amount": "5.00"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            InventoryItem.objects.filter(name="Cooking Oil").exists()
        )

    def test_edit_inventory_item(self):
        response = self.client.post(
            reverse("inventory_edit", args=[self.item.pk]),
            {
                "name": "Flour",
                "category": "Ingredients",
                "quantity": "15.00",
                "unit": "lbs",
                "cost": "12.00",
                "low_stock_amount": "10.00"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.item.refresh_from_db()
        self.assertEqual(self.item.quantity, Decimal("15.00"))

    def test_delete_inventory_item(self):
        response = self.client.post(
            reverse("inventory_delete", args=[self.item.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            InventoryItem.objects.filter(pk=self.item.pk).exists()
        )

    def test_delete_requires_confirmation(self):
        self.client.get(
            reverse("inventory_delete", args=[self.item.pk])
        )

        self.assertTrue(
            InventoryItem.objects.filter(pk=self.item.pk).exists()
        )

    def test_low_stock_below_threshold(self):
        self.assertTrue(self.item.is_low_stock)

        response = self.client.get(reverse("inventory_list"))
        self.assertContains(response, "Low Stock")

    def test_low_stock_at_threshold(self):
        self.item.quantity = Decimal("10.00")
        self.item.save()

        self.assertTrue(self.item.is_low_stock)

    def test_not_low_stock(self):
        self.item.quantity = Decimal("20.00")
        self.item.save()

        self.assertFalse(self.item.is_low_stock)

    def test_negative_quantity_rejected(self):
        response = self.client.post(
            reverse("inventory_create"),
            {
                "name": "Invalid Quantity",
                "category": "Ingredients",
                "quantity": "-5.00",
                "unit": "lbs",
                "cost": "10.00",
                "low_stock_amount": "5.00"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            InventoryItem.objects.filter(name="Invalid Quantity").exists()
        )

    def test_negative_cost_rejected(self):
        response = self.client.post(
            reverse("inventory_create"),
            {
                "name": "Invalid Cost",
                "category": "Ingredients",
                "quantity": "10.00",
                "unit": "lbs",
                "cost": "-10.00",
                "low_stock_amount": "5.00"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            InventoryItem.objects.filter(name="Invalid Cost").exists()
        )

    def test_negative_threshold_rejected(self):
        response = self.client.post(
            reverse("inventory_create"),
            {
                "name": "Invalid Threshold",
                "category": "Ingredients",
                "quantity": "10.00",
                "unit": "lbs",
                "cost": "10.00",
                "low_stock_amount": "-5.00"
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            InventoryItem.objects.filter(name="Invalid Threshold").exists()
        )


class EventManagementTests(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name="Boise Food Festival",
            location="Boise, Idaho",
            event_date=date(2026, 11, 15),
            application_deadline=date(2026, 11, 1),
            application_fee=Decimal("50.00"),
            application_status="Not Applied",
            notes="Food trailer event"
        )

    def test_event_creation(self):
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(self.event.name, "Boise Food Festival")

    def test_event_page_loads(self):
        response = self.client.get(reverse("event_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boise Food Festival")

    def test_event_detail_page(self):
        response = self.client.get(
            reverse("event_detail", args=[self.event.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Boise, Idaho")

    def test_create_event(self):
        response = self.client.post(
            reverse("event_create"),
            {
                "name": "Nampa Food Fair",
                "location": "Nampa, Idaho",
                "event_date": "2026-12-10",
                "application_deadline": "2026-11-20",
                "application_fee": "25.00",
                "application_status": "Applied",
                "notes": "New event"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Event.objects.filter(name="Nampa Food Fair").exists()
        )

    def test_edit_event(self):
        response = self.client.post(
            reverse("event_edit", args=[self.event.pk]),
            {
                "name": "Updated Food Festival",
                "location": "Boise, Idaho",
                "event_date": "2026-11-15",
                "application_deadline": "2026-11-01",
                "application_fee": "75.00",
                "application_status": "Applied",
                "notes": "Updated event"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.event.refresh_from_db()
        self.assertEqual(self.event.name, "Updated Food Festival")
        self.assertEqual(
            self.event.application_fee,
            Decimal("75.00")
        )

    def test_delete_event(self):
        response = self.client.post(
            reverse("event_delete", args=[self.event.pk])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            Event.objects.filter(pk=self.event.pk).exists()
        )

    def test_delete_requires_confirmation(self):
        self.client.get(
            reverse("event_delete", args=[self.event.pk])
        )

        self.assertTrue(
            Event.objects.filter(pk=self.event.pk).exists()
        )

    def test_application_status_update(self):
        response = self.client.post(
            reverse("event_edit", args=[self.event.pk]),
            {
                "name": self.event.name,
                "location": self.event.location,
                "event_date": "2026-11-15",
                "application_deadline": "2026-11-01",
                "application_fee": "50.00",
                "application_status": "Accepted",
                "notes": self.event.notes
            }
        )

        self.assertEqual(response.status_code, 302)

        self.event.refresh_from_db()
        self.assertEqual(
            self.event.application_status,
            "Accepted"
        )

    def test_application_deadline(self):
        self.assertEqual(
            self.event.application_deadline,
            date(2026, 11, 1)
        )

        response = self.client.get(
            reverse("event_detail", args=[self.event.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nov. 1, 2026")

    def test_negative_application_fee_rejected(self):
        response = self.client.post(
            reverse("event_create"),
            {
                "name": "Invalid Event",
                "location": "Boise",
                "event_date": "2026-11-15",
                "application_deadline": "2026-11-01",
                "application_fee": "-50.00",
                "application_status": "Not Applied",
                "notes": ""
            }
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Application fee cannot be negative."
        )
        self.assertFalse(
            Event.objects.filter(name="Invalid Event").exists()
        )

    def test_event_status_choices(self):
        expected_statuses = [
            "Not Applied",
            "Applied",
            "Accepted",
            "Rejected",
            "Attending"
        ]

        actual_statuses = [
            choice[0] for choice in Event.STATUS_CHOICES
        ]

        self.assertEqual(actual_statuses, expected_statuses)



# ==========================================
# Checkpoint 4: Sales and Expense Tests
# ==========================================

from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.db.models import ProtectedError

from .models import MenuItem, Event, Sale, Expense


class SalesManagementTests(TestCase):

    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name="Corn Dog",
            category="Food",
            description="Regular corn dog",
            price=Decimal("6.00"),
            available=True
        )

        self.event = Event.objects.create(
            name="Boise Food Festival",
            location="Boise",
            event_date=date(2026, 11, 20),
            application_deadline=date(2026, 11, 10),
            application_fee=Decimal("100.00"),
            application_status="Accepted",
            notes=""
        )

        self.sale_data = {
            "menu_item": self.menu_item.pk,
            "event": self.event.pk,
            "quantity": 3,
            "unit_price": "6.00",
            "sale_date": "2026-11-20",
        }

    def create_sale(self):
        return Sale.objects.create(
            menu_item=self.menu_item,
            event=self.event,
            quantity=3,
            unit_price=Decimal("6.00"),
            sale_date=date(2026, 11, 20)
        )

    # 1. Sales page loads
    def test_sales_page_loads(self):
        response = self.client.get(reverse("sale_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/sales.html")

    # 2. Add Sale form loads
    def test_sale_create_page_loads(self):
        response = self.client.get(reverse("sale_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/sale_form.html")

    # 3. Create a sale associated with an event
    def test_create_sale(self):
        response = self.client.post(
            reverse("sale_create"),
            self.sale_data
        )

        self.assertRedirects(response, reverse("sale_list"))
        self.assertEqual(Sale.objects.count(), 1)

        sale = Sale.objects.first()

        self.assertEqual(sale.menu_item, self.menu_item)
        self.assertEqual(sale.event, self.event)
        self.assertEqual(sale.quantity, 3)
        self.assertEqual(sale.unit_price, Decimal("6.00"))

    # 4. Create sale without an event
    def test_create_sale_without_event(self):
        data = self.sale_data.copy()
        data["event"] = ""

        response = self.client.post(
            reverse("sale_create"),
            data
        )

        self.assertRedirects(response, reverse("sale_list"))
        self.assertIsNone(Sale.objects.first().event)

    # 5. Edit an existing sale
    def test_edit_sale(self):
        sale = self.create_sale()

        data = self.sale_data.copy()
        data["quantity"] = 10
        data["unit_price"] = "7.50"

        response = self.client.post(
            reverse("sale_edit", args=[sale.pk]),
            data
        )

        self.assertRedirects(response, reverse("sale_list"))

        sale.refresh_from_db()

        self.assertEqual(sale.quantity, 10)
        self.assertEqual(sale.unit_price, Decimal("7.50"))

    # 6. Delete a sale
    def test_delete_sale(self):
        sale = self.create_sale()

        url = reverse("sale_delete", args=[sale.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.count(), 1)

        response = self.client.post(url)

        self.assertRedirects(response, reverse("sale_list"))
        self.assertEqual(Sale.objects.count(), 0)

    # 7. Reject zero and negative quantities
    def test_invalid_sale_quantity(self):
        for quantity in [0, -5]:
            with self.subTest(quantity=quantity):
                data = self.sale_data.copy()
                data["quantity"] = quantity

                response = self.client.post(
                    reverse("sale_create"),
                    data
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(Sale.objects.count(), 0)
                self.assertIn(
                    "quantity",
                    response.context["form"].errors
                )

    # 8. Reject negative prices
    def test_negative_sale_price(self):
        data = self.sale_data.copy()
        data["unit_price"] = "-5.00"

        response = self.client.post(
            reverse("sale_create"),
            data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Sale.objects.count(), 0)
        self.assertIn(
            "unit_price",
            response.context["form"].errors
        )

    # 9. A menu item with recorded sales cannot be deleted
    def test_sale_protects_menu_item(self):
        self.create_sale()

        with self.assertRaises(ProtectedError):
            self.menu_item.delete()

        self.assertTrue(
            MenuItem.objects.filter(
                pk=self.menu_item.pk
            ).exists()
        )

    # 10. Deleting an event preserves associated sales
    def test_delete_event_preserves_sale(self):
        sale = self.create_sale()

        self.event.delete()
        sale.refresh_from_db()

        self.assertIsNone(sale.event)
        self.assertEqual(Sale.objects.count(), 1)


class ExpenseManagementTests(TestCase):

    def setUp(self):
        self.event = Event.objects.create(
            name="Boise Food Festival",
            location="Boise",
            event_date=date(2026, 11, 20),
            application_deadline=date(2026, 11, 10),
            application_fee=Decimal("100.00"),
            application_status="Accepted",
            notes=""
        )

        self.expense_data = {
            "description": "Flour",
            "category": "Ingredients",
            "store": "WinCo",
            "quantity": "2",
            "amount": "15.98",
            "date": "2026-11-15",
            "event": self.event.pk,
            "notes": "Two bags of flour",
        }

    def create_expense(self):
        return Expense.objects.create(
            description="Flour",
            category="Ingredients",
            store="WinCo",
            quantity=Decimal("2.00"),
            amount=Decimal("15.98"),
            date=date(2026, 11, 15),
            event=self.event,
            notes="Two bags of flour"
        )

    # 1. Expenses page loads
    def test_expenses_page_loads(self):
        response = self.client.get(reverse("expense_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/expenses.html")

    # 2. Add Expense form loads
    def test_expense_create_page_loads(self):
        response = self.client.get(reverse("expense_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "dashboard/expense_form.html")

        self.assertContains(response, "WinCo")

    # 3. Create a food expense from WinCo
    def test_create_food_expense(self):
        response = self.client.post(
            reverse("expense_create"),
            self.expense_data
        )

        self.assertRedirects(response, reverse("expense_list"))
        self.assertEqual(Expense.objects.count(), 1)

        expense = Expense.objects.first()

        self.assertEqual(expense.description, "Flour")
        self.assertEqual(expense.category, "Ingredients")
        self.assertEqual(expense.store, "WinCo")
        self.assertEqual(expense.quantity, Decimal("2.00"))
        self.assertEqual(expense.amount, Decimal("15.98"))
        self.assertEqual(expense.event, self.event)

        response = self.client.get(reverse("expense_list"))
        self.assertContains(response, "WinCo")
        self.assertContains(response, "Flour")

    # 4. Create an event fee without a store
    def test_create_event_fee(self):
        data = self.expense_data.copy()

        data["description"] = "Festival Vendor Fee"
        data["category"] = "Event Fee"
        data["store"] = ""
        data["quantity"] = "1"
        data["amount"] = "150.00"

        response = self.client.post(
            reverse("expense_create"),
            data
        )

        self.assertRedirects(response, reverse("expense_list"))

        expense = Expense.objects.first()

        self.assertEqual(expense.category, "Event Fee")
        self.assertEqual(expense.store, "")
        self.assertEqual(expense.amount, Decimal("150.00"))
        self.assertEqual(expense.event, self.event)

    # 5. Edit an expense
    def test_edit_expense(self):
        expense = self.create_expense()

        data = self.expense_data.copy()
        data["description"] = "Cooking Oil"
        data["store"] = "US CHEF'STORE"
        data["amount"] = "42.50"

        response = self.client.post(
            reverse("expense_edit", args=[expense.pk]),
            data
        )

        self.assertRedirects(response, reverse("expense_list"))

        expense.refresh_from_db()

        self.assertEqual(expense.description, "Cooking Oil")
        self.assertEqual(expense.store, "US CHEF'STORE")
        self.assertEqual(expense.amount, Decimal("42.50"))

    # 6. Delete an expense
    def test_delete_expense(self):
        expense = self.create_expense()

        url = reverse("expense_delete", args=[expense.pk])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 1)

        response = self.client.post(url)

        self.assertRedirects(response, reverse("expense_list"))
        self.assertEqual(Expense.objects.count(), 0)

    # 7. Reject zero and negative quantities
    def test_invalid_expense_quantity(self):
        for quantity in ["0", "-2"]:
            with self.subTest(quantity=quantity):
                data = self.expense_data.copy()
                data["quantity"] = quantity

                response = self.client.post(
                    reverse("expense_create"),
                    data
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(Expense.objects.count(), 0)
                self.assertIn(
                    "quantity",
                    response.context["form"].errors
                )

    # 8. Reject negative expenses
    def test_negative_expense_amount(self):
        data = self.expense_data.copy()
        data["amount"] = "-20.00"

        response = self.client.post(
            reverse("expense_create"),
            data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 0)
        self.assertIn(
            "amount",
            response.context["form"].errors
        )

    # 9. Reject invalid expense categories
    def test_invalid_expense_category(self):
        data = self.expense_data.copy()
        data["category"] = "Invalid Category"

        response = self.client.post(
            reverse("expense_create"),
            data
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Expense.objects.count(), 0)
        self.assertIn(
            "category",
            response.context["form"].errors
        )

    # 10. Deleting an event preserves expenses
    def test_delete_event_preserves_expense(self):
        expense = self.create_expense()

        self.event.delete()
        expense.refresh_from_db()

        self.assertIsNone(expense.event)
        self.assertEqual(Expense.objects.count(), 1)


# ==========================================
# Checkpoint 5: Financial Calculation Tests
# ==========================================

from .finance import calculate_finances


class FinancialCalculationTests(TestCase):

    def setUp(self):
        self.item = MenuItem.objects.create(
            name="Corn Dog",
            category="Food",
            price=Decimal("6.50"),
            available=True
        )

        self.event1 = Event.objects.create(
            name="Boise Festival",
            location="Boise",
            event_date=date(2026, 11, 20),
            application_deadline=date(2026, 11, 10),
            application_fee=Decimal("100.00"),
            application_status="Accepted"
        )

        self.event2 = Event.objects.create(
            name="Downtown Market",
            location="Boise",
            event_date=date(2026, 11, 21),
            application_deadline=date(2026, 11, 11),
            application_fee=Decimal("50.00"),
            application_status="Accepted"
        )

        # Event 1: 3 x $6.50 = $19.50
        self.sale1 = Sale.objects.create(
            menu_item=self.item,
            event=self.event1,
            quantity=3,
            unit_price=Decimal("6.50"),
            sale_date=date(2026, 11, 20)
        )

        # Event 2: 2 x $10 = $20.00
        Sale.objects.create(
            menu_item=self.item,
            event=self.event2,
            quantity=2,
            unit_price=Decimal("10.00"),
            sale_date=date(2026, 11, 21)
        )

        # Business sale without an event: $5.00
        Sale.objects.create(
            menu_item=self.item,
            event=None,
            quantity=1,
            unit_price=Decimal("5.00"),
            sale_date=date(2026, 11, 22)
        )

        # Expenses: $4.50 + $7.00 + $3.00
        for description, amount, event in [
            ("Flour", "4.50", self.event1),
            ("Supplies", "7.00", self.event2),
            ("Fuel", "3.00", None),
        ]:
            Expense.objects.create(
                description=description,
                category="Ingredients",
                store="WinCo",
                quantity=Decimal("1.00"),
                amount=Decimal(amount),
                date=date(2026, 11, 20),
                event=event
            )

    # Test 1: Financial summary loads
    def test_financial_page_loads(self):
        response = self.client.get(
            reverse("financial_summary")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "dashboard/finances.html"
        )

    # Test 2: Total business revenue
    def test_total_revenue(self):
        totals = calculate_finances()

        self.assertEqual(
            totals["revenue"],
            Decimal("44.50")
        )

    # Test 3: Total business expenses
    def test_total_expenses(self):
        totals = calculate_finances()

        self.assertEqual(
            totals["expenses"],
            Decimal("14.50")
        )

    # Test 4: Total estimated profit
    def test_total_profit(self):
        totals = calculate_finances()

        self.assertEqual(
            totals["profit"],
            Decimal("30.00")
        )

    # Test 5: Event 1 calculation
    def test_event_one_profit(self):
        totals = calculate_finances(self.event1)

        self.assertEqual(
            totals["revenue"],
            Decimal("19.50")
        )
        self.assertEqual(
            totals["expenses"],
            Decimal("4.50")
        )
        self.assertEqual(
            totals["profit"],
            Decimal("15.00")
        )

    # Test 6: Event 2 calculation
    def test_event_two_profit(self):
        totals = calculate_finances(self.event2)

        self.assertEqual(
            totals["revenue"],
            Decimal("20.00")
        )
        self.assertEqual(
            totals["expenses"],
            Decimal("7.00")
        )
        self.assertEqual(
            totals["profit"],
            Decimal("13.00")
        )

    # Test 7: Filtering by event
    def test_event_filter(self):
        response = self.client.get(
            reverse("financial_summary"),
            {"event": self.event1.pk}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["totals"]["profit"],
            Decimal("15.00")
        )
        self.assertContains(
            response, "Boise Festival"
        )

    # Test 8: Invalid events return 404
    def test_invalid_event(self):
        for value in ["invalid", "999999"]:
            with self.subTest(event=value):
                response = self.client.get(
                    reverse("financial_summary"),
                    {"event": value}
                )
                self.assertEqual(
                    response.status_code, 404
                )

    # Test 9: Empty records return zero
    def test_empty_finances(self):
        Sale.objects.all().delete()
        Expense.objects.all().delete()

        totals = calculate_finances()

        self.assertEqual(
            totals["revenue"],
            Decimal("0.00")
        )
        self.assertEqual(
            totals["expenses"],
            Decimal("0.00")
        )
        self.assertEqual(
            totals["profit"],
            Decimal("0.00")
        )

    # Test 10: Updating sales changes profit
    def test_profit_updates_after_sale_edit(self):
        self.sale1.quantity = 5
        self.sale1.save()

        totals = calculate_finances(self.event1)

        self.assertEqual(
            totals["revenue"],
            Decimal("32.50")
        )
        self.assertEqual(
            totals["profit"],
            Decimal("28.00")
        )


# Boise 2027 vendor opportunities may have unpublished dates and fees.
class EventOptionalInfoTests(TestCase):
    def test_event_can_be_saved_without_unpublished_details(self):
        event = Event.objects.create(
            name="Unannounced Event",
            location="Boise, Idaho",
        )
        self.assertIsNone(event.event_date)
        self.assertIsNone(event.application_deadline)
        self.assertIsNone(event.application_fee)

    def test_events_display_tbd_for_unpublished_details(self):
        event = Event.objects.create(
            name="Unannounced Event",
            location="Boise, Idaho",
        )
        response = self.client.get(reverse("event_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, event.name)
        self.assertContains(response, "TBD")
