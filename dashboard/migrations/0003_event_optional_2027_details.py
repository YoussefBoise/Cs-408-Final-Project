# Generated for 2027 vendor opportunities with unpublished dates or fees.
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_expense_quantity_expense_store_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="event_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="application_deadline",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="application_fee",
            field=models.DecimalField(
                max_digits=10, decimal_places=2, blank=True, null=True
            ),
        ),
    ]
