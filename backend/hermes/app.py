from edgy import Instance, monkay
from esmerald import Esmerald, Include

from .db import get_db_connection


def get_application():
    registry = get_db_connection()

    # ensure the settings are loaded
    monkay.evaluate_settings(ignore_import_errors=False)

    app = registry.asgi(
        Esmerald(
            routes=[Include(namespace="hermes.urls")],
            settings_module="hermes.settings.Settings",
        )
    )

    monkay.set_instance(Instance(registry=registry, app=app))
    return app


app = get_application()
