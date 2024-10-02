from peewee import *
from peewee import SqliteDatabase

db = SqliteDatabase('database.db')


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = db
        order_by = 'id'


class User(BaseModel):
    tg_id = IntegerField(unique=True)
    name = CharField(max_length=50)

class Pyment(BaseModel):
    beer = IntegerField()
    cigarettes = IntegerField()
    pyment_data = DateField()
    user_id = ForeignKeyField(User)

    class Meta:
        db_table = 'payments'


async def create_new_tables():
    with db:
        db.create_tables([User, Pyment])

