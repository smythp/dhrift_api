from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry


DB = PostgresEngine(
    config={
        "database": "driftt",
        "user": "driftt_admin",
        "password": "superdh",
        "host": "localhost",
        "port": 5432,
    }
)

APP_REGISTRY = AppRegistry(apps=["driftt.piccolo_app", "piccolo_admin.piccolo_app"])
