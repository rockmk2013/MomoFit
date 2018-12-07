from django.db import models
from django.db import connection
from django.contrib.auth.models import AbstractUser

from cloudinary.models import CloudinaryField
from django.db import connection
import pandas as pd
import datetime as dt
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
        cursor.execute("SELECT * from train_freq where user_id=%s and gr_date > CURDATE()- INTERVAL 49 DAY ;",[self.id])
        row = cursor.fetchall()
        #print(row)
        if len(row) == 0:
            train_first_day = None
            freq_count = None
        else:    
            data = pd.DataFrame(list(row),columns=["gr_id","gr_date","gym_id","user_id"])
            data['train_first_day'] = data['gr_date'].apply(lambda x : x - dt.timedelta(days=x.isoweekday() % 7))
            tr_data = data[['train_first_day','gr_id']].groupby(['train_first_day']).agg(['count']).reset_index()
            train_first_day = tr_data['train_first_day']
            freq_count = tr_data['gr_id']['count'].tolist()
        return train_first_day,freq_count

    def get_records(self):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM train_success WHERE user_id=%s and train_date BETWEEN SUBDATE(CURDATE(), INTERVAL 49 DAY) AND CURDATE() order by train_date;",[self.id])
        row = cursor.fetchall()

        if len(row) == 0:
            week_first_day = None
            success_rate = None
        else:    
            data = pd.DataFrame(list(row),columns=["id","item_id","menu_set","menu_rep","menu_weight","date","rep","weight","train_set"])
            data['week_first_day'] = data['date'].apply(lambda x : x - dt.timedelta(days=x.isoweekday() % 7))
            data['menu_rep'] = data['menu_rep'].apply(lambda x : int(x))
            data['success rate'] = (data['rep']*data['weight']*data['train_set']) / (data['menu_rep']*data['menu_weight']*data['menu_set'])
            tr_data = data[['week_first_day','success rate']].groupby(['week_first_day']).agg(['mean']).reset_index()
            week_first_day = tr_data['week_first_day']
            success_rate = tr_data['success rate']['mean'].tolist()
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
            #print(row)
            data = pd.DataFrame(list(row),
                                columns=["id", "weight", "fat", "date"])
            data['week_first_day'] = data['date'].apply(lambda x: x - dt.timedelta(days=x.isoweekday() % 7))
            tr_data = data[['week_first_day', 'weight', 'fat']].groupby(['week_first_day']).agg(['mean']).reset_index()
            week_first_day = tr_data['week_first_day']
            weight = tr_data['weight']['mean'].tolist()
            fat = tr_data['fat']['mean'].tolist()
            weight = [ round(elem, 2) for elem in weight]
            fat = [ round(elem, 2) for elem in fat]
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
        cursor.execute("select menu.menu_id,item_list.item_name from menu,item_list where menu.item_id=item_list.item_id and user_id=%s and display<>1;",[self.id])
        row = cursor.fetchall()
        return row

    def get_menu(self):
        cursor = connection.cursor()
        cursor.execute("select item_name,item_type,menu_set,menu_rep,menu_weight,menu_id from menu,item_list where menu.item_id=item_list.item_id and user_id=%s and display=1;",[self.id])
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
    train_date = models.DateField(db_column='train_date', null=False)
    rep = models.IntegerField(db_column='rep', null=False)
    weight = models.FloatField(db_column='weight', null=False)
    train_set = models.IntegerField(db_column='train_set', null=False)
    gr_id = models.ForeignKey(GymRecord, on_delete=models.CASCADE, db_column='gr_id')
    item_id = models.ForeignKey(ItemList, on_delete=models.CASCADE, db_column='item_id')

    class Meta:
        db_table = 'train_record'

    def get_record(self):
        cursor = connection.cursor()
        cursor.execute("select tr.train_date, gym_list.name, item_list.item_name, tr.rep, tr.weight, tr.train_set from train_record as tr, item_list, gym_record, gym_list where tr.item_id=item_list.item_id and gym_record.gr_id = tr.gr_id and gym_list.gym_id=gym_record.gym_id and gym_record.user_id=%s order by tr.train_date desc limit 7;",[self.id])
        row = cursor.fetchall()
        return row

    def search(self,date):
        cursor = connection.cursor()
        cursor.execute("select tr.train_date, gym_list.name, item_list.item_name, tr.rep, tr.weight, tr.train_set from train_record as tr, item_list, gym_record, gym_list where tr.item_id=item_list.item_id and gym_record.gr_id = tr.gr_id and gym_list.gym_id=gym_record.gym_id and gym_record.user_id=%s and tr.train_date=%s;",[self.id,date])
        row = cursor.fetchall()
        return row
    
    def get_item_list(self):
        cursor = connection.cursor()
        cursor.execute("select item_list.item_name from item_list;")
        row = cursor.fetchall()
        return row

    def get_gym_list(self):
        cursor = connection.cursor()
        cursor.execute("select distinct gym_list.name from gym_list;")
        row = cursor.fetchall()
        return row

    def add_record(self, _date, _gym, _item, _rep, _weight, _train_set):
        ### without sp
        cursor = connection.cursor()
        # add gym_record
        cursor.execute("select gym_id from gym_list where gym_list.name=%s;",[_gym])
        _gym_id = cursor.fetchall()
        cursor.execute("insert into gym_record (user_id, gym_id, gr_date) values (%s,%s,%s);",[self.id, _gym_id, _date])
        
        # add train_record
        cursor.execute("select item_id from item_list where item_list.item_name=%s;",[_item])
        _item_id = cursor.fetchall()
        cursor.execute("select gr_id from gym_record where gym_record.gym_id = %s and gym_record.gr_date = %s and gym_record.user_id = %s;",[_gym_id, _date, self.id])
        _gr_id = cursor.fetchall()
        
        cursor.execute("insert into train_record (train_date,rep,weight,train_set,gr_id,item_id) values (%s,%s,%s,%s,%s,%s);",[_date,_rep,_weight,_train_set,_gr_id,_item_id])


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
    fr_date = models.DateField(db_column='fr_date',default=False)

    class Meta:
        db_table = 'food_record'

    def get_record(self):
        cursor = connection.cursor()
        cursor.execute("select fr.fr_date,store.store_name,fi.food,fr.quantity,fi.kcal from food_record as fr,food_item as fi,store where fi.food_id=fr.food_id and store.store_id=fi.store_id and fr.id=%s order by fr.fr_date desc limit 7;",[self.id])
        row = cursor.fetchall()
        return row

    def get_food_list(self):
        cursor = connection.cursor()
        cursor.execute("select store.store_name,food_item.food from store,food_item where store.store_id = food_item.store_id")
        row = cursor.fetchall()
        return row

    def search(self,date):
        cursor = connection.cursor()
        cursor.execute("select fr.fr_date,fi.food,fr.quantity,fi.kcal from food_record as fr,food_item as fi where fi.food_id=fr.food_id and fr.id=%s and fr.fr_date=%s;",[self.id,date])
        row = cursor.fetchall()
        return row

    def add(self):
        cursor = connection.cursor()
        
    def __str__(self):
        return self.fr_id