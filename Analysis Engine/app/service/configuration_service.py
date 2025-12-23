from app.configuration.analysis_configuration import get_customer_analysis_settings, get_transaction_analysis_settings
from app.configuration.connections_configuration import get_database_connection_settings, get_broker_connection_settings, get_engine_database_connection_settings, get_sanctions_connection_countries_settings
from app.configuration.schema_configuration import get_schema_configuration_settings
from app.configuration.websocket_configuration import get_websocket_settings

from app.configuration.analysis_configuration import set_customer_analysis_settings, set_transaction_analysis_settings
from app.configuration.connections_configuration import set_database_connection_settings, set_broker_connection_settings, set_engine_database_connection_settings, set_sanctionlist_watchlist_countries_settings
from app.configuration.schema_configuration import set_schema_configuration_settings
from app.configuration.websocket_configuration import set_websocket_settings

def get_all_configurations():
    confs = {
        "Data Analysis Configurations" : {
            "Transaction Related Analysis": get_transaction_analysis_settings(),
            "Customer Related Analysis": get_customer_analysis_settings()
        },
        "Connection Configurations" : {
            "Central/Core Database Settings": get_database_connection_settings(),
            "Realtime Data Source Settings": get_broker_connection_settings(),
            "Engine Storage": get_engine_database_connection_settings(),
            "Other Settings": get_sanctions_connection_countries_settings()
        },
        "Central/Core Database Data Schema Mapping": get_schema_configuration_settings(),
        "Webhook Configurations": get_websocket_settings()
    }

    return confs


def update_configuration(new_config):
    print("[Update Configuration] Called ...")

    if "Data_Analysis_Configurations" in new_config:
        data_analysis = new_config["Data_Analysis_Configurations"]
        
        if "Transaction_Related_Analysis" in data_analysis:
            set_transaction_analysis_settings(data_analysis["Transaction_Related_Analysis"])
            
        if "Customer_Related_Analysis" in data_analysis:
            set_customer_analysis_settings(data_analysis["Customer_Related_Analysis"])

    
    if "Connection_Configurations" in new_config:
        connection_configs = new_config["Connection_Configurations"]
        
        if "Central_Core_Database_Settings" in connection_configs:
            set_database_connection_settings(connection_configs["Central_Core_Database_Settings"])
            
        if "Realtime_Data_Source_Settings" in connection_configs:
            set_broker_connection_settings(connection_configs["Realtime_Data_Source_Settings"])
            
        if "Engine_Storage" in connection_configs:
            set_engine_database_connection_settings(connection_configs["Engine_Storage"])
            
        if "Other_Settings" in connection_configs:
            set_sanctionlist_watchlist_countries_settings(connection_configs["Other_Settings"])

    if "Central_Core_Database_Data_Schema_Mapping" in new_config:
        set_schema_configuration_settings(new_config["Central_Core_Database_Data_Schema_Mapping"])
        
    if "Webhook_Configurations" in new_config:
        set_websocket_settings(new_config["Webhook_Configurations"])
        
    return (new_config)
