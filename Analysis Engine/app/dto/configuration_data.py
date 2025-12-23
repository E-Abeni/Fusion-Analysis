from pydantic import BaseModel
from typing import Optional, Dict


class TransactionRelatedAnalysis(BaseModel):
    """Transaction Analysis Settings."""
    Transaction_Amount_Analysis: Optional[str] = None
    Transaction_Frequency_Analysis: Optional[str] = None
    Transaction_Turnover_Analysis: Optional[str] = None
    BrentFord_Digit_Analysis: Optional[str] = None
    Round_Number_Hoarding_Analysis: Optional[str] = None
    Transaction_Geographic_Analysis: Optional[str] = None

class CustomerRelatedAnalysis(BaseModel):
    """Customer Analysis Settings."""
    Peer_Group_Analysis: Optional[str] = None
    Peer_Group_Analysis_Threshold: Optional[str] = None 
    Anomaly_Detection: Optional[str] = None
    Anomaly_Detection_Sensitivity: Optional[str] = None 
    Time_Gap_Analysis: Optional[str] = None
    Time_Gap_Threshold_Seconds: Optional[str] = None 
    KYC_Integrity_Check: Optional[str] = None
    Sanctions_List_Check: Optional[str] = None
    Watchlist_Check: Optional[str] = None
    Geographic_Risk_Assessment: Optional[str] = None

class DataAnalysisConfigurations(BaseModel):
    """Main container for Data Analysis settings."""
    Transaction_Related_Analysis: Optional[TransactionRelatedAnalysis] = None
    Customer_Related_Analysis: Optional[CustomerRelatedAnalysis] = None



class CoreDatabaseSettings(BaseModel):
    """Central/Core Database Settings."""
    database_type: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None # Stored as string
    database_name: Optional[str] = None
    table_name: Optional[str] = None
    connection_string: Optional[str] = None

class RealtimeDataSourceSettings(BaseModel):
    """Realtime Data Source Settings (Kafka/etc.)."""
    bootstrap_server: Optional[str] = None
    topic: Optional[str] = None
    group_id: Optional[str] = None
    auto_offset_reset: Optional[str] = None

class EngineStorageSettings(BaseModel):
    """Engine Storage Settings."""
    engine_database_type: Optional[str] = None
    engine_username: Optional[str] = None
    engine_password: Optional[str] = None
    engine_host: Optional[str] = None
    engine_port: Optional[str] = None # Stored as string
    engine_database_name: Optional[str] = None
    engine_connection_string: Optional[str] = None

class OtherSettings(BaseModel):
    """Miscellaneous Connection Settings."""
    sanctions_table_name: Optional[str] = None
    watchlist_table_name: Optional[str] = None
    high_risk_countries_table_name: Optional[str] = None

class ConnectionConfigurations(BaseModel):
    """Main container for Connection settings."""
    Central_Core_Database_Settings: Optional[CoreDatabaseSettings] = None
    Realtime_Data_Source_Settings: Optional[RealtimeDataSourceSettings] = None
    Engine_Storage: Optional[EngineStorageSettings] = None
    Other_Settings: Optional[OtherSettings] = None




class DataSchemaMapping(BaseModel):
    TRANSACTIONID: Optional[str] = None
    REPORTNO: Optional[str] = None
    REPORTDATE: Optional[str] = None
    BRANCHID: Optional[str] = None
    BRANCHNAME: Optional[str] = None
    TRANSACTIONDATE: Optional[str] = None
    TRANSACTIONTIME: Optional[str] = None
    TRANSACTIONTYPE: Optional[str] = None
    CONDUCTINGMANNER: Optional[str] = None
    CURRENCYTYPE: Optional[str] = None
    AMOUNTINBIRR: Optional[str] = None
    AMOUNTINCURRENCY: Optional[str] = None
    FULL_NAME: Optional[str] = None
    OTHERNAME: Optional[str] = None
    SEX: Optional[str] = None
    BIRTHDATE: Optional[str] = None
    IDCARDNO: Optional[str] = None
    PASSPORTNO: Optional[str] = None
    PASSPORTISSUEDBY: Optional[str] = None
    RESIDENCECOUNTRY: Optional[str] = None
    ORIGINCOUNTRY: Optional[str] = None
    OCCUPATION: Optional[str] = None
    COUNTRY: Optional[str] = None
    REGION: Optional[str] = None
    CITY: Optional[str] = None
    SUBCITY: Optional[str] = None
    WOREDA: Optional[str] = None
    HOUSENO: Optional[str] = None
    POSTALCODE: Optional[str] = None
    BUSINESSMOBILENO: Optional[str] = None
    BUSSINESSTELNO: Optional[str] = None
    BUSINESSFAXNO: Optional[str] = None
    RESIDENCETELNO: Optional[str] = None
    EMAILADDRESS: Optional[str] = None
    ACCOUNTNO: Optional[str] = None
    ACCHOLDERBRANCH: Optional[str] = None
    ACCOWNERNAME: Optional[str] = None
    ACCOUNTTYPE: Optional[str] = None
    OPENEDDATE: Optional[str] = None
    BALANCEHELD: Optional[str] = None
    BALANCEHELDDATE: Optional[str] = None
    CLOSEDDATE: Optional[str] = None
    BENFULLNAME: Optional[str] = None
    BENACCOUNTNO: Optional[str] = None
    BENBRANCHID: Optional[str] = None
    BENBRANCHNAME: Optional[str] = None
    BENOWNERENTITY: Optional[str] = None
    BENCOUNTRY: Optional[str] = None
    BENREGION: Optional[str] = None
    BENCITY: Optional[str] = None
    BENZONE: Optional[str] = None
    BENWOREDA: Optional[str] = None
    BENHOUSENO: Optional[str] = None
    BENTELNO: Optional[str] = None
    BENISENTITY: Optional[str] = None

class WebhookConfigurations(BaseModel):
    """Webhook Settings."""
    websocket_host: Optional[str] = None
    websocket_port: Optional[str] = None # Stored as string
    use_ssl: Optional[str] = None
    send_interval: Optional[str] = None # Stored as string


class SettingsRootDTO(BaseModel):
  
    Data_Analysis_Configurations: Optional[DataAnalysisConfigurations] = None
    Connection_Configurations: Optional[ConnectionConfigurations] = None
    Central_Core_Database_Data_Schema_Mapping: Optional[DataSchemaMapping] = None
    Webhook_Configurations: Optional[WebhookConfigurations] = None