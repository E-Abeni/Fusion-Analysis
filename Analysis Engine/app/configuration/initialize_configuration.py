import app.configuration.analysis_configuration as ac
import app.configuration.connections_configuration as cc
import app.configuration.schema_configuration as sc
import app.configuration.websocket_configuration as wc
import pprint

def initialize_configuration():
    cas = {
        'Peer Group Analysis': 'True',
        'Peer Group Analysis Threshold': '0.75',
        'Anomaly Detection': 'True',
        'Anomaly Detection Sensitivity': '3',
        'Time Gap Analysis': 'False',
        'Time Gap Threshold Seconds': '900',
        'KYC Integrity Check': 'True',
        'Sanctions List Check': 'True',
        'Watchlist Check': 'True',
        'Geographic Risk Assessment': 'True'
    }
    tas = {
        'Transaction Amount Analysis': 'True',
        'Transaction Frequency Analysis': 'True',
        'Transaction Turnover Analysis': 'False',
        'BrentFord Digit Analysis': 'True',
        'Round Number Hoarding Analysis': 'True',
        'Transaction Geographic Analysis': 'True'
    }
    ac.set_customer_analysis_settings(cas)
    ac.set_transaction_analysis_settings(tas)



    dcs = {
        "database_type": "postgres",
        "database_username": "postgres",
        "database_password": "admin",
        "database_host": "localhost",
        "database_port": "5432",
        "database_name": "postgres",
        "table_name": "test_transactions",
        "database_connection_string": "postgresql://postgres:admin@localhost:5432/postgres"

    }
    bcs = {
        "bootstrap_server": "kafka-broker1:9092,kafka-broker2:9092",
        "topic": "transactions_in",
        "group_id": "analysis_consumer_group",
        "auto_offset_reset": "latest"
    }
    edcs = {
        "engine_database_type": "postgres",
        "engine_username": "postgres",
        "engine_password": "admin",
        "engine_host": "localhost",
        "engine_port": "5432",
        "engine_database_name": "postgres",
        "engine_connection_string": "postgresql://postgres:admin@localhost:5432/postgres"
    }
    swcs = {
        "sanctions_table_name": "ofac_sanctions",
        "watchlist_table_name": "internal_watchlist",
        "high_risk_countries_table_name": "high_risk_geographies"
    }
    cc.set_database_connection_settings(dcs)
    cc.set_broker_connection_settings(bcs)
    cc.set_engine_database_connection_settings(edcs)
    cc.set_sanctionlist_watchlist_countries_settings(swcs)


    '''
    scs = {
        "TRANSACTIONID": "TRANSACTIONID",
        "REPORTNO": "REPORTNO",
        "REPORTDATE": "REPORTDATE",
        "BRANCHID": "BRANCHID",
        "BRANCHNAME": "BRANCHNAME",
        "TRANSACTIONDATE": "TRANSACTIONDATE",
        "TRANSACTIONTIME": "TRANSACTIONTIME",
        "TRANSACTIONTYPE": "TRANSACTIONTYPE",
        "CONDUCTINGMANNER": "CONDUCTINGMANNER",
        "CURRENCYTYPE": "CURRENCYTYPE",
        "AMOUNTINBIRR": "AMOUNTINBIRR",
        "AMOUNTINCURRENCY": "AMOUNTINCURRENCY",
        "FULL_NAME": "FULL_NAME",
        "OTHERNAME": "OTHERNAME",
        "SEX": "SEX",
        "BIRTHDATE": "BIRTHDATE",
        "IDCARDNO": "IDCARDNO",
        "PASSPORTNO": "PASSPORTNO",
        "PASSPORTISSUEDBY": "PASSPORTISSUEDBY",
        "RESIDENCECOUNTRY": "RESIDENCECOUNTRY",
        "ORIGINCOUNTRY": "ORIGINCOUNTRY",
        "OCCUPATION": "OCCUPATION",
        "COUNTRY": "COUNTRY",
        "REGION": "REGION",
        "CITY": "CITY",
        "SUBCITY": "SUBCITY",
        "WOREDA": "WOREDA",
        "HOUSENO": "HOUSENO",
        "POSTALCODE": "POSTALCODE",
        "BUSINESSMOBILENO": "BUSINESSMOBILENO",
        "BUSSINESSTELNO": "BUSSINESSTELNO",
        "BUSINESSFAXNO": "BUSINESSFAXNO",
        "RESIDENCETELNO": "RESIDENCETELNO",
        "EMAILADDRESS": "EMAILADDRESS",
        "ACCOUNTNO": "ACCOUNTNO",
        "ACCHOLDERBRANCH": "ACCHOLDERBRANCH",
        "ACCOWNERNAME": "ACCOWNERNAME",
        "ACCOUNTTYPE": "ACCOUNTTYPE",
        "OPENEDDATE": "OPENEDDATE",
        "BALANCEHELD": "BALANCEHELD",
        "BALANCEHELDDATE": "BALANCEHELDDATE",
        "CLOSEDDATE": "CLOSEDDATE",
        "BENFULLNAME": "BENFULLNAME",
        "BENACCOUNTNO": "BENACCOUNTNO",
        "BENBRANCHID": "BENBRANCHID",
        "BENBRANCHNAME": "BENBRANCHNAME",
        "BENOWNERENTITY": "BENOWNERENTITY",
        "BENCOUNTRY": "BENCOUNTRY",
        "BENREGION": "BENREGION",
        "BENCITY": "BENCITY",
        "BENZONE": "BENZONE",
        "BENWOREDA": "BENWOREDA",
        "BENHOUSENO": "BENHOUSENO",
        "BENTELNO": "BENTELNO",
        "BENISENTITY": "BENISENTITY"
    }
    '''

    scs = {
        "TRANSACTIONID": "transactionid",
        "REPORTNO": "reportno",
        "REPORTDATE": "reportdate",
        "BRANCHID": "branchid",
        "BRANCHNAME": "branchname",
        "TRANSACTIONDATE": "transactiondate",
        "TRANSACTIONTIME": "transactiontime",
        "TRANSACTIONTYPE": "transactiontype",
        "CONDUCTINGMANNER": "conductingmanner",
        "CURRENCYTYPE": "currencytype",
        "AMOUNTINBIRR": "amountinbirr",
        "AMOUNTINCURRENCY": "amountincurrency",
        "FULL_NAME": "full_name",
        "OTHERNAME": "othername",
        "SEX": "sex",
        "BIRTHDATE": "birthdate",
        "IDCARDNO": "idcardno",
        "PASSPORTNO": "passportno",
        "PASSPORTISSUEDBY": "passportissuedby",
        "RESIDENCECOUNTRY": "residencecountry",
        "ORIGINCOUNTRY": "origincountry",
        "OCCUPATION": "occupation",
        "COUNTRY": "country",
        "REGION": "region",
        "CITY": "city",
        "SUBCITY": "subcity",
        "WOREDA": "woreda",
        "HOUSENO": "houseno",
        "POSTALCODE": "postalcode",
        "BUSINESSMOBILENO": "businessmobileno",
        "BUSSINESSTELNO": "bussinesstelno",
        "BUSINESSFAXNO": "businessfaxno",
        "RESIDENCETELNO": "residencetelno",
        "EMAILADDRESS": "emailaddress",
        "ACCOUNTNO": "accountno",
        "ACCHOLDERBRANCH": "accholderbranch",
        "ACCOWNERNAME": "accownername",
        "ACCOUNTTYPE": "accounttype",
        "OPENEDDATE": "openeddate",
        "BALANCEHELD": "balanceheld",
        "BALANCEHELDDATE": "balancehelddate",
        "CLOSEDDATE": "closeddate",
        "BENFULLNAME": "benfullname",
        "BENACCOUNTNO": "benaccountno",
        "BENBRANCHID": "benbranchid",
        "BENBRANCHNAME": "benbranchname",
        "BENOWNERENTITY": "benownerentity",
        "BENCOUNTRY": "bencountry",
        "BENREGION": "benregion",
        "BENCITY": "bencity",
        "BENZONE": "benzone",
        "BENWOREDA": "benworeda",
        "BENHOUSENO": "benhouseno",
        "BENTELNO": "bentelno",
        "BENISENTITY": "benisentity",
        "BANKID": "bankid",
        "TRANSACTIONDATE_PARTITION": "transactiondate_partition"
    }

    wcs = {
        "websocket_host": "0.0.0.0",
        "websocket_port": "8080",
        "use_ssl": "True",
        "send_interval": "5"
    }
    sc.set_schema_configuration_settings(scs)
    wc.set_websocket_settings(wcs)



if __name__ == "__main__":
    initialize_configuration()
    print("Configuration initialization complete.")
    print("\n++++++++++++++++ Customer Analysis Settings ++++++++++++++++\n")
    pprint.pprint(ac.get_customer_analysis_settings())
    print("\n++++++++++++++++ Transaction Analysis Settings ++++++++++++++++\n")
    pprint.pprint(ac.get_transaction_analysis_settings())
    print("\n++++++++++++++++ Database Connection Settings ++++++++++++++++\n")
    pprint.pprint(cc.get_database_connection_settings())
    print("\n++++++++++++++++ Broker Connection Settings ++++++++++++++++\n")
    pprint.pprint(cc.get_broker_connection_settings())
    print("\n++++++++++++++++ Engine Database Connection Settings ++++++++++++++++\n")
    pprint.pprint(cc.get_engine_database_connection_settings())
    print("\n++++++++++++++++ Sanctionlist Watchlist Countries Settings ++++++++++++++++\n")
    pprint.pprint(cc.get_sanctions_connection_countries_settings())
    print("\n++++++++++++++++ Schema Configuration Settings ++++++++++++++++\n")
    pprint.pprint(sc.get_schema_configuration_settings())
    print("\n++++++++++++++++ Websocket Configuration Settings ++++++++++++++++\n")
    pprint.pprint(wc.get_websocket_settings())