
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
