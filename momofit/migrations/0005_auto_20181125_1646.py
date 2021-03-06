# Generated by Django 2.1.3 on 2018-11-25 08:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('momofit', '0004_auto_20181124_0218'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.IntegerField(verbose_name='身高(cm)')),
                ('weight', models.IntegerField(verbose_name='體重(kg)')),
                ('push_pr', models.IntegerField(default=15, verbose_name='胸推個人紀錄(kg)')),
                ('squat_pr', models.IntegerField(default=15, verbose_name='深蹲個人紀錄(kg)')),
                ('lift_pr', models.IntegerField(default=15, verbose_name='硬舉個人紀錄(kg)')),
                ('tdee', models.IntegerField(default=1200)),
                ('actlevel', models.IntegerField(choices=[(1, '久坐'), (2, '輕量活動量'), (3, '中度活動量'), (4, '高度活動量'), (5, '非常高度活動量')], default=1, verbose_name='個人活動量')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('menu_weight', models.FloatField()),
                ('menu_set', models.IntegerField()),
                ('menu_rep', models.CharField(max_length=5)),
                ('items', models.ManyToManyField(to='momofit.ItemList')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='height',
        ),
        migrations.RemoveField(
            model_name='user',
            name='kcal',
        ),
        migrations.RemoveField(
            model_name='user',
            name='weight',
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=20, verbose_name='年齡'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(1, '生理男性'), (2, '生理女性')], default=1, verbose_name='性別'),
        ),
    ]
