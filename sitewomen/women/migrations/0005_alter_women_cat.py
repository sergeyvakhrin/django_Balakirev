# Generated by Django 5.1 on 2024-11-02 17:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0004_category_women_cat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='women',
            name='cat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='women.category'),
            preserve_default=False,
        ),
    ]
