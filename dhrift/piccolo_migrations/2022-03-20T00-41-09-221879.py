from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Date
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.indexes import IndexMethod


ID = "2022-03-20T00:41:09:221879"
VERSION = "0.71.1"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="dhrift", description=DESCRIPTION
    )

    manager.add_table("DrifttUser", tablename="dhrift_user")

    manager.add_column(
        table_class_name="DrifttUser",
        tablename="dhrift_user",
        column_name="first_name",
        db_column_name="first_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="DrifttUser",
        tablename="dhrift_user",
        column_name="last_name",
        db_column_name="last_name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="DrifttUser",
        tablename="dhrift_user",
        column_name="email",
        db_column_name="email",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    manager.add_column(
        table_class_name="DrifttUser",
        tablename="dhrift_user",
        column_name="last_modified",
        db_column_name="last_modified",
        column_class_name="Date",
        column_class=Date,
        params={
            "default": DateNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
    )

    return manager
