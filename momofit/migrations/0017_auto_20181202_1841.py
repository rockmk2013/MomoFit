# Generated by Django 2.1.3 on 2018-12-02 10:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('momofit', '0016_auto_20181202_1838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='items',
            field=models.ForeignKey(db_column='item_id', on_delete=django.db.models.deletion.CASCADE, to='momofit.ItemList'),
        ),
    ]