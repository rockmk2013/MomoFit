from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    # add additional fields in here
    age = models.IntegerField(help_text='Enter age', default=20)
    sex = models.CharField(default='Male', max_length=5)
    height = models.IntegerField(default=160)
    weight = models.IntegerField(default=60)
    kcal = models.IntegerField(default=1500)

    def __str__(self):
        return self.email


class GymList(models.Model):
    gym_id = models.IntegerField(db_column='gym_id', primary_key=True)
    name = models.CharField(db_column='gym_name', max_length=30, null=False)
    address = models.CharField(db_column='address', max_length=100, null=False)
    program = models.CharField(db_column='program', max_length=30, null=False)

    class Meta:
        db_table = 'gym_list'

    def __str__(self):
        return self.name


class GymRecord(models.Model):
    gr_id = models.IntegerField(db_column='gr_id', primary_key=True)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='user_id', null=False)
    gym_id = models.ForeignKey(GymList, on_delete=models.CASCADE, db_column='gym_id', null=False)
    gr_date = models.DateTimeField(db_column='gr_date', null=False)

    class Meta:
        db_table = 'gym_record'

    def __str__(self):
        return self.gr_id


class ItemList(models.Model):
    item_id = models.IntegerField(db_column='item_id', primary_key=True)
    item_name = models.CharField(db_column='item_name', max_length=30, null=False)
    item_type = models.CharField(db_column='item_type', max_length=30, null=False)

    class Meta:
        db_table = 'item_list'

    def __str__(self):
        return self.item_name

class TrainRecord(models.Model):
    train_id = models.IntegerField(db_column='train_id', primary_key=True)
    train_date = models.DateTimeField(db_column='train_date', null=False)
    rep = models.IntegerField(db_column='rep', null=False)
    weight = models.FloatField(db_column='weight', null=False)
    train_set = models.IntegerField(db_column='train_set', null=False)
    gr_id = models.ForeignKey(GymRecord, on_delete=models.CASCADE, db_column='gr_id')
    item_id = models.ForeignKey(ItemList, on_delete=models.CASCADE, db_column='item_id')

    class Meta:
        db_table = 'train_record'

    def __str__(self):
        return self.train_id