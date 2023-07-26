import datetime
from peewee import SqliteDatabase, Model, CharField, TextField, DateTimeField, BooleanField, ForeignKeyField

db = SqliteDatabase('dhrift.db')

class BaseModel(Model):
    class Meta:
        database = db




class DrifttUser(BaseModel):
    first_name = CharField()
    last_name = CharField()
    username = CharField(unique=True)
    password = CharField()
    confirmed = BooleanField
    email = CharField()
    created = DateTimeField(default=datetime.datetime.now)
    last_modified = DateTimeField(default=datetime.datetime.now)


class Site(BaseModel):
    display_name = CharField()
    institution = CharField()
    admin = ForeignKeyField(DrifttUser, backref='sites')

    domain = CharField()
    created = DateTimeField(default=datetime.datetime.now)
    last_modified = DateTimeField(default=datetime.datetime.now)

# class ResourceType(str, enum.Enum):
#     workshop = "workshop"
#     guide = "guide"
#     insight = "insight"
#     other = "other"


class Resource(BaseModel):
    title = CharField()
    # author = ForeignKey(DrifttUser)
    content = TextField
    # type = CharField(choices=ResourceType)
    created = DateTimeField(default=datetime.datetime.now)
    last_modified = DateTimeField(default=datetime.datetime.now)


tables =[
    DrifttUser,
    Site,
    Resource
    ]


db.create_tables(tables)

with db.atomic() as transaction:  # Opens new transaction.
    DrifttUser.create(
        first_name = "pat",
        last_name = "Smyth",
        username = "paddy",
        password = "sosecret",
        confirmed = True,
        email = "foo@example.com")
