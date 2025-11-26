from app.configuration import Configuration


configuration = Configuration ("configuration/kv_store.db")


def get_database_connection_settings():
    return {
        'database_type': configuration.get("database_type"),
        'username': configuration.get("database_username"),
        'password': configuration.get("database_password"),
        'host': configuration.get("database_host"),
        'port': configuration.get("database_port"),
        'database_name': configuration.get("database_name"),
        'connection_string': configuration.get("database_connection_string")
    }

def set_database_connection_settings(connection_parameters):
    configuration.set("database_type", connection_parameters.get('database_type', ''))
    configuration.set("database_username", connection_parameters.get('username', ''))
    configuration.set("database_password", connection_parameters.get('password', ''))
    configuration.set("database_host", connection_parameters.get('host', ''))
    configuration.set("database_port", connection_parameters.get('port', ''))
    configuration.set("database_name", connection_parameters.get('database_name', ''))
    configuration.set("database_connection_string", connection_parameters.get('connection_string', ''))

    return {
        "message": "success",
        "setting": connection_parameters
    }

def get_broker_connection_settings():
    return (
        {
            'bootstrap_server': configuration.get("bootstrap_server"),
            'topic': configuration.get("topic"),
            "group_id": configuration.get("group_id"),
            "auto_offset_reset": configuration.get("auto_offset_reset")
        }
    ) 

def set_broker_connection_settings(broker_parameters):
    configuration.set("bootstrap_server", broker_parameters.get('bootstrap_server', ''))
    configuration.set("topic", broker_parameters.get('topic', ''))
    configuration.set("group_id", broker_parameters.get('group_id', ''))
    configuration.set("auto_offset_reset", broker_parameters.get('auto_offset_reset', ''))

    return {
        "message": "success",
        "setting": broker_parameters
    }


def get_engine_database_connection_settings():
    return {
        'engine_database_type': configuration.get("engine_database_type"),
        'engine_username': configuration.get("engine_username"),
        'engine_password': configuration.get("engine_password"),
        'engine_host': configuration.get("engine_host"),
        'engine_port': configuration.get("engine_port"),
        'engine_database_name': configuration.get("engine_database_name"),
        'engine_connection_string': configuration.get("engine_connection_string")
    }

def set_engine_database_connection_settings(engine_connection_parameters):
    configuration.set("engine_database_type", engine_connection_parameters.get('engine_database_type', ''))
    configuration.set("engine_username", engine_connection_parameters.get('engine_username', ''))
    configuration.set("engine_password", engine_connection_parameters.get('engine_password', ''))
    configuration.set("engine_host", engine_connection_parameters.get('engine_host', ''))
    configuration.set("engine_port", engine_connection_parameters.get('engine_port', ''))
    configuration.set("engine_database_name", engine_connection_parameters.get('engine_database_name', ''))
    configuration.set("engine_connection_string", engine_connection_parameters.get('engine_connection_string', ''))

    return {
        "message": "success",
        "setting": engine_connection_parameters
    }


def get_sanctions_connection_countries_settings():
    return {
        "sanctions_table_name": configuration.get("sanctions_table_name"),
        "watchlist_table_name": configuration.get("watchlist_table_name"),
        "high_risk_countries_table_name": configuration.get("high_risk_countries_table_name")
    }

def set_sanctionlist_watchlist_countries_settings(sanctions_parameters):
    configuration.set("sanctions_table_name", sanctions_parameters.get('sanctions_table_name', ''))
    configuration.set("watchlist_table_name", sanctions_parameters.get('watchlist_table_name', '')),
    configuration.set("high_risk_countries_table_name", sanctions_parameters.get('high_risk_countries_table_name', ''))

    return {
        "message": "success",
        "setting": sanctions_parameters
    }