from django.db import models
from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField

# Create your models here.

class User(AbstractUser):
    # add additional fields in here
    age = models.IntegerField(verbose_name="年齡", default=20)
    sex_status = (
        (1,'生理男性'),
        (2,'生理女性'),
    )
    sex = models.IntegerField(default=1,choices=sex_status,verbose_name="性別")
    user_pic = CloudinaryField('image',null=True)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email

class History(models.Model):
    height = models.IntegerField(verbose_name="身高(cm)")
    weight = models.IntegerField(verbose_name="體重(kg)")
    fat = models.FloatField(verbose_name="體脂率(%)",null=True)
    push_pr = models.IntegerField(verbose_name="胸推個人紀錄(kg)",default=15)
    squat_pr = models.IntegerField(verbose_name="深蹲個人紀錄(kg)",default=15)
    lift_pr = models.IntegerField(verbose_name="硬舉個人紀錄(kg)",default=15)
    tdee = models.IntegerField(default=1200)

    actlevel_status = (
        (1,'久坐'),
        (2,'輕量活動量'),
        (3,'中度活動量'),
        (4,'高度活動量'),
        (5,'非常高度活動量'),
    )

    actlevel = models.IntegerField(
        choices=actlevel_status, 
        default=1, 
        verbose_name="個人活動量"
    )
    user= models.ForeignKey(User, on_delete=models.CASCADE,null=True,db_column='user_id')
    
    class Meta:
        db_table = 'history'

class Menu(models.Model):
    menu_weight = models.FloatField()
    menu_set = models.IntegerField()
    menu_rep = models.CharField(max_length=5)
    items = models.ManyToManyField('ItemList')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,db_column='user_id')

    class Meta:
        db_table = 'menu'

class GymList(models.Model):
    gym_id = models.AutoField(db_column='gym_id', primary_key=True)
    name = models.CharField(db_column='name', max_length=30, null=False)
    address = models.CharField(db_column='address', max_length=100, null=False)
    program = models.CharField(db_column='program', max_length=30, null=False)

    class Meta:
        db_table = 'gym_list'

    def __str__(self):
        return self.name


class GymRecord(models.Model):
    gr_id = models.AutoField(db_column='gr_id', primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', null=False)
    gym_id = models.ForeignKey(GymList, on_delete=models.CASCADE, db_column='gym_id', null=False)
    gr_date = models.DateTimeField(db_column='gr_date', null=False)

    class Meta:
        db_table = 'gym_record'

    def __str__(self):
        return self.gr_id


class ItemList(models.Model):
    item_id = models.AutoField(db_column='item_id', primary_key=True)
    item_name = models.CharField(db_column='item_name', max_length=30, null=False)
    item_type = models.CharField(db_column='item_type', max_length=30, null=False)

    class Meta:
        db_table = 'item_list'

    def __str__(self):
        return self.item_name

class TrainRecord(models.Model):
    train_id = models.AutoField(db_column='train_id', primary_key=True)
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

class Store(models.Model):
    store_id = models.AutoField(db_column='store_id', primary_key=True)  # Field name made lowercase.
    store_name = models.CharField(db_column='store_name', max_length=50)  # Field name made lowercase.
    address = models.CharField(db_column='address', max_length=50)  # Field name made lowercase.

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.store_name

class FoodItem(models.Model):
    food_id = models.AutoField(db_column='food_id', primary_key=True)  # Field name made lowercase.
    food = models.CharField(db_column='food', max_length=50)  # Field name made lowercase.
    kcal = models.FloatField(db_column='kcal')  # Field name made lowercase.
    store = models.ForeignKey(Store, models.DO_NOTHING, db_column='store_id')  # Field name made lowercase.

    class Meta:
        db_table = 'food_item'

    def __str__(self):
        return self.food_id


class FoodRecord(models.Model):
    fr_id = models.AutoField(db_column='fr_id', primary_key=True)  # Field name made lowercase.
    food_id = models.ForeignKey(FoodItem, models.DO_NOTHING, db_column='food_id')  # Field name made lowercase.
    quantity = models.FloatField(db_column='quantity')  # Field name made lowercase.
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='id')  # Field name made lowercase.

    class Meta:
        db_table = 'food_record'

    def __str__(self):
        return self.fr_id