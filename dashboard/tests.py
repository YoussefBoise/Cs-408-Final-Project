
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from .models import MenuItem, InventoryItem, Event, Sale, Expense
from datetime import date


class PageTests(TestCase):

    def test_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Food Trailer Management')
        self.assertContains(response, 'Dashboard')


class ModelTests(TestCase):

    def test_menu_item(self):
        item = MenuItem.objects.create(
            name='Corn Dog',
            category='Food',
            price=Decimal('5.00')
        )
        self.assertEqual(item.name, 'Corn Dog')

    def test_inventory_item(self):
        item = InventoryItem.objects.create(
            name='Flour',
            category='Ingredients',
            quantity=Decimal('10.00'),
            unit='lbs',
            cost=Decimal('2.50'),
            low_stock_amount=Decimal('3.00')
        )
        self.assertEqual(item.quantity, Decimal('10.00'))

    def test_event(self):
        event = Event.objects.create(
            name='Food Festival',
            location='Boise',
            event_date=date(2026, 11, 10),
            application_deadline=date(2026, 11, 1),
            application_fee=Decimal('50.00')
        )
        self.assertEqual(event.application_status, 'Not Applied')

    def test_sale(self):
        item = MenuItem.objects.create(
            name='Corn Dog',
            category='Food',
            price=Decimal('5.00')
        )
        sale = Sale.objects.create(
            menu_item=item,
            quantity=2,
            unit_price=Decimal('5.00'),
            sale_date=date(2026, 10, 18)
        )
        self.assertEqual(sale.quantity, 2)

    def test_expense(self):
        expense = Expense.objects.create(
            description='Propane',
            category='Supplies',
            amount=Decimal('30.00'),
            date=date(2026, 10, 18)
        )
        self.assertEqual(expense.amount, Decimal('30.00'))
