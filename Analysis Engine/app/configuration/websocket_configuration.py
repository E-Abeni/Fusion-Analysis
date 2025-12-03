from app.configuration.configuration import Configuration

configuration = Configuration ("kv_store.db")

def get_websocket_settings():
    return {
        'websocket_host': configuration.get("websocket_host"),
        'websocket_port': configuration.get("websocket_port"),
        'use_ssl': configuration.get("use_ssl"),
        'send_interval': configuration.get("send_interval")
    }


def set_websocket_settings(websocket_parameters):
    configuration.set("websocket_host", websocket_parameters.get('websocket_host', ''))
    configuration.set("websocket_port", websocket_parameters.get('websocket_port', ''))
    configuration.set("use_ssl", websocket_parameters.get('use_ssl', ''))
    configuration.set("send_interval", websocket_parameters.get('send_interval', ''))

    return {
        "message": "success",
        "setting": websocket_parameters
    }