# Generated by Django 2.1.3 on 2018-12-09 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('momofit', '0033_auto_20181209_0117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        # migrations.AlterField(
        #     model_name='history',
        #     name='fat',
        #     field=models.FloatField(verbose_name='體脂率(%)'),
        # ),
        # migrations.AlterField(
        #     model_name='history',
        #     name='user',
        #     field=models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        # ),
    ]
