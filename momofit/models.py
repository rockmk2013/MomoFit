from django.db import models
from django.db import connection
from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField
from django.db import connection
import pandas as pd
import datetime as dt

class User(AbstractUser):
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
    date = models.DateTimeField(auto_now_add=True,null=True)

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

    def get_history(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM history where user_id = %s;",[self.id])
        row = cursor.fetchall()
        return row


    @staticmethod
    def add_history(height, weight, push_pr, squat_pr, lift_pr, actlevel, user_id, fat, date):
        cur = connection.cursor()
        cur.callproc('add_history', (height, weight, push_pr, squat_pr, lift_pr, actlevel, user_id, fat, date))
        results = cur.fetchall()
        cur.close()
        return results

    def get_train_freq(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * from train_freq where user_id=%s  ;",[self.id])
        row = cursor.fetchall()
        #print(row)
        if len(row) == 0:
            train_first_day = None
            freq_count = None
        else:    
            data = pd.DataFrame(list(row),columns=["train_first_day","train_date","user_id"])
            tr_data = data[['train_first_day','train_date']].groupby(['train_first_day']).agg(['count']).reset_index()
            train_first_day = tr_data['train_first_day']
            freq_count = tr_data['train_date']['count'].tolist()
        return train_first_day,freq_count

    def get_records(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM train_success WHERE user_id=%s ;",[self.id])
        row = cursor.fetchall()

        if len(row) == 0:
            week_first_day = None
            success_rate = None
        else:    
            data = pd.DataFrame(list(row),columns=["id","item_id","success_rate","week_first_day"])
            tr_data = data[['week_first_day','success_rate']].groupby(['week_first_day']).agg(['mean']).reset_index()
            week_first_day = tr_data['week_first_day']
            success_rate = tr_data['success_rate']['mean'].tolist()
            success_rate = [ round(elem, 2) for elem in success_rate]

            for i, rate in enumerate(success_rate):
                if rate > 1:
                    success_rate[i] = 1
                success_rate[i] *= 100

        return week_first_day, success_rate

    def get_weight_fat(self):
        cursor = connection.cursor()
        cursor.execute(
            "SELECT * FROM get_weight WHERE user_id=%s ;",
            [self.id])
        row = cursor.fetchall()

        if len(row) == 0:
            week_first_day = None
            weight = None
            fat = None
        else:
            data = pd.DataFrame(list(row),columns=["id", "weight", "fat", "week_first_day"])
            week_first_day = data['week_first_day']
            weight = [ int(elem) for elem in data['weight'].tolist()]
            fat = [ int(elem) for elem in data['fat'].tolist()]
        return week_first_day, weight, fat


class Menu(models.Model):
    menu_id = models.AutoField(db_column='menu_id', primary_key=True)
    menu_weight = models.FloatField()
    menu_set = models.IntegerField()
    menu_rep = models.IntegerField()
    items = models.ForeignKey('ItemList', on_delete=models.CASCADE,db_column='item_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE,db_column='user_id')
    display = models.BooleanField(default=False)

    class Meta:
        db_table = 'menu'
    
    def get_item_list(self):
        cursor = connection.cursor()
        cursor.execute("select menu.menu_id,item.item_name from menu,item where menu.item_id=item.item_id and user_id=%s and display<>1;",[self.id])
        row = cursor.fetchall()
        return row

    def get_menu(self):
        cursor = connection.cursor()
        cursor.execute("select item_name,item_type,menu_set,menu_rep,menu_weight,menu_id from menu,item where menu.item_id=item.item_id and user_id=%s and display=1;",[self.id])
        row = cursor.fetchall()
        return row

    def delete_menu_item(self):
        cursor = connection.cursor()
        cursor.execute("update menu set display=0 where menu_id=%s",[self])

    def add_menu_item(self):
        cursor = connection.cursor()
        cursor.execute("update menu set display=1 where menu_id in %s",[tuple(self)])

    @staticmethod
    def create_menu(self):
        # print(type(self.id))
        cur = connection.cursor()
        cur.callproc('CreateMenu_procedure', (self.id,))
        cur.close()

class ItemList(models.Model):
    item_id = models.AutoField(db_column='item_id', primary_key=True)
    item_name = models.CharField(db_column='item_name', max_length=30, null=False)
    item_type = models.CharField(db_column='item_type', max_length=30, null=False)

    class Meta:
        db_table = 'item'

    def __str__(self):
        return self.item_name

class TrainRecord(models.Model):
    train_id = models.AutoField(db_column='train_id', primary_key=True)
    train_date = models.DateField(db_column='train_date', null=False)
    rep = models.IntegerField(db_column='rep', null=False)
    weight = models.FloatField(db_column='weight', null=False)
    train_set = models.IntegerField(db_column='train_set', null=False)
    gym_name = models.CharField(db_column='gym_name', max_length=30, null=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    item_id = models.ForeignKey(ItemList, on_delete=models.CASCADE, db_column='item_id')

    class Meta:
        db_table = 'train_record'

    def get_record(self):
        cursor = connection.cursor()
        cursor.execute("select tr.train_date,tr.gym_name,item.item_name,tr.rep,tr.weight,tr.train_set,tr.train_id from train_record as tr,item where tr.item_id=item.item_id and tr.user_id=%s order by tr.train_date desc limit 7;",[self.id])
        row = cursor.fetchall()
        return row

    def search(self,date):
        cursor = connection.cursor()
        cursor.execute("select tr.train_date,tr.gym_name,item.item_name,tr.rep,tr.weight,tr.train_set from train_record as tr,item where tr.item_id=item.item_id and tr.user_id=%s and tr.train_date=%s;",[self.id, date])
        row = cursor.fetchall()
        return row
    
    def get_item_list(self):
        cursor = connection.cursor()
        cursor.execute("select item.item_id,item.item_name from item;")
        row = cursor.fetchall()
        return row

    def add_record(self, _date, _gym, _item, _rep, _weight, _train_set):
        cursor = connection.cursor()
        cursor.execute("insert into train_record (train_date,rep,weight,train_set,item_id,user_id,gym_name) values (%s,%s,%s,%s,%s,%s,%s);",[_date,_rep,_weight,_train_set,_item,self.id, _gym]) 

    def delete_train_record(self,_train_id):
        cursor = connection.cursor()
        cursor.execute("delete from train_record where train_id=%s",[_train_id])

    def __str__(self):
        return self.train_id

class Store(models.Model):
    store_id = models.AutoField(db_column='store_id', primary_key=True)
    store_name = models.CharField(db_column='store_name', max_length=50)
    address = models.CharField(db_column='address', max_length=50)

    class Meta:
        db_table = 'store'

    def __str__(self):
        return self.store_name

class FoodItem(models.Model):
    food_id = models.AutoField(db_column='food_detail_id', primary_key=True)
    food = models.CharField(db_column='food_name', max_length=50)
    kcal = models.FloatField(db_column='kcal')
    store = models.ForeignKey(Store, models.DO_NOTHING, db_column='store_id')

    class Meta:
        db_table = 'food_detail'

    def __str__(self):
        return self.food_id


class FoodRecord(models.Model):
    fr_id = models.AutoField(db_column='food_id', primary_key=True)
    food_id = models.ForeignKey(FoodItem, models.DO_NOTHING, db_column='food_detail_id')
    quantity = models.FloatField(db_column='quantity')
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='user_id')
    fr_date = models.DateField(db_column='fr_date',default=False)

    class Meta:
        db_table = 'food'

    def get_record(self):
        cursor = connection.cursor()
        cursor.execute("select fr.fr_date,store.store_name,fi.food_name,fr.quantity,fi.kcal,fr.food_id,store.address from food as fr,food_detail as fi,store where fi.food_detail_id=fr.food_detail_id and store.store_id=fi.store_id and fr.user_id=%s order by fr.fr_date desc limit 7;",[self.id])
        row = cursor.fetchall()
        return row

    def get_food_list(self):
        cursor = connection.cursor()
        cursor.execute("select store.store_name,food_detail.food_name from store,food_detail where store.store_id = food_detail.store_id")
        row = cursor.fetchall()
        return row

    def search(self,date):
        cursor = connection.cursor()
        cursor.execute("select fr.fr_date,store.store_name,fi.food_name,fr.quantity,fi.kcal,store.address from food as fr,food_detail as fi,store where fi.food_detail_id=fr.food_detail_id and fr.user_id=%s and store.store_id=fi.store_id and fr.fr_date=%s;",[self.id,date])
        row = cursor.fetchall()
        return row

    def add_record(self, _date, _food, _quantity):
        cursor = connection.cursor()
        cursor.execute("select food_detail_id from food_detail where food_name = %s;",[_food])
        _food_detail_id = cursor.fetchall()
        cursor.execute("insert into food (quantity,food_detail_id,user_id,fr_date) values (%s,%s,%s,%s);",[_quantity,_food_detail_id,self.id,_date])

    def delete_food_record(self,_food_id):
        cursor = connection.cursor()
        cursor.execute("delete from food where food_id=%s;",[_food_id])

    def __str__(self):
        return self.fr_id