from app.configuration import Configuration

configuration = Configuration ("configuration/kv_store.db")


def get_schema_configuration_settings():
    return {
        'TRANSACTIONID': configuration.get("TRANSACTIONID"),
        'REPORTNO': configuration.get("REPORTNO"),
        'REPORTDATE': configuration.get("REPORTDATE"),
        'BRANCHID': configuration.get("BRANCHID"),
        'BRANCHNAME': configuration.get("BRANCHNAME"),
        'TRANSACTIONDATE': configuration.get("TRANSACTIONDATE"),
        'TRANSACTIONTIME': configuration.get("TRANSACTIONTIME"),
        'TRANSACTIONTYPE': configuration.get("TRANSACTIONTYPE"),
        'CONDUCTINGMANNER': configuration.get("CONDUCTINGMANNER"),
        'CURRENCYTYPE': configuration.get("CURRENCYTYPE"),
        'AMOUNTINBIRR': configuration.get("AMOUNTINBIRR"),
        'AMOUNTINCURRENCY': configuration.get("AMOUNTINCURRENCY"),
        'FULL_NAME': configuration.get("FULL_NAME"),
        'OTHERNAME': configuration.get("OTHERNAME"),
        'SEX': configuration.get("SEX"),
        'BIRTHDATE': configuration.get("BIRTHDATE"),
        'IDCARDNO': configuration.get("IDCARDNO"),
        'PASSPORTNO': configuration.get("PASSPORTNO"),
        'PASSPORTISSUEDBY': configuration.get("PASSPORTISSUEDBY"),
        'RESIDENCECOUNTRY': configuration.get("RESIDENCECOUNTRY"),
        'ORIGINCOUNTRY': configuration.get("ORIGINCOUNTRY"),
        'OCCUPATION': configuration.get("OCCUPATION"),
        'COUNTRY': configuration.get("COUNTRY"),
        'REGION': configuration.get("REGION"),
        'CITY': configuration.get("CITY"),
        'SUBCITY': configuration.get("SUBCITY"),
        'WOREDA': configuration.get("WOREDA"),
        'HOUSENO': configuration.get("HOUSENO"),
        'POSTALCODE': configuration.get("POSTALCODE"),
        'BUSINESSMOBILENO': configuration.get("BUSINESSMOBILENO"),
        'BUSSINESSTELNO': configuration.get("BUSSINESSTELNO"),
        'BUSINESSFAXNO': configuration.get("BUSINESSFAXNO"),
        'RESIDENCETELNO': configuration.get("RESIDENCETELNO"),
        'EMAILADDRESS': configuration.get("EMAILADDRESS"),
        'ACCOUNTNO': configuration.get("ACCOUNTNO"),
        'ACCHOLDERBRANCH': configuration.get("ACCHOLDERBRANCH"),
        'ACCOWNERNAME': configuration.get("ACCOWNERNAME"),
        'ACCOUNTTYPE': configuration.get("ACCOUNTTYPE"),
        'OPENEDDATE': configuration.get("OPENEDDATE"),
        'BALANCEHELD': configuration.get("BALANCEHELD"),
        'BALANCEHELDDATE': configuration.get("BALANCEHELDDATE"),
        'CLOSEDDATE': configuration.get("CLOSEDDATE"),
        'BENFULLNAME': configuration.get("BENFULLNAME"),
        'BENACCOUNTNO': configuration.get("BENACCOUNTNO"),
        'BENBRANCHID': configuration.get("BENBRANCHID"),
        'BENBRANCHNAME': configuration.get("BENBRANCHNAME"),
        'BENOWNERENTITY': configuration.get("BENOWNERENTITY"),
        'BENCOUNTRY': configuration.get("BENCOUNTRY"),
        'BENREGION': configuration.get("BENREGION"),
        'BENCITY': configuration.get("BENCITY"),
        'BENZONE': configuration.get("BENZONE"),
        'BENWOREDA': configuration.get("BENWOREDA"),
        'BENHOUSENO': configuration.get("BENHOUSENO"),
        'BENTELNO': configuration.get("BENTELNO"),
        'BENISENTITY': configuration.get("BENISENTITY")
    }


def set_schema_configuration_settings(schema_parameters):
    configuration.set("TRANSACTIONID", schema_parameters.get('TRANSACTIONID', ''))
    configuration.set("REPORTNO", schema_parameters.get('REPORTNO', ''))
    configuration.set("REPORTDATE", schema_parameters.get('REPORTDATE', ''))
    configuration.set("BRANCHID", schema_parameters.get('BRANCHID', ''))
    configuration.set("BRANCHNAME", schema_parameters.get('BRANCHNAME', ''))
    configuration.set("TRANSACTIONDATE", schema_parameters.get('TRANSACTIONDATE', ''))
    configuration.set("TRANSACTIONTIME", schema_parameters.get('TRANSACTIONTIME', ''))
    configuration.set("TRANSACTIONTYPE", schema_parameters.get('TRANSACTIONTYPE', ''))
    configuration.set("CONDUCTINGMANNER", schema_parameters.get('CONDUCTINGMANNER', ''))
    configuration.set("CURRENCYTYPE", schema_parameters.get('CURRENCYTYPE', ''))
    configuration.set("AMOUNTINBIRR", schema_parameters.get('AMOUNTINBIRR', ''))
    configuration.set("AMOUNTINCURRENCY", schema_parameters.get('AMOUNTINCURRENCY', ''))
    configuration.set("FULL_NAME", schema_parameters.get('FULL_NAME', ''))
    configuration.set("OTHERNAME", schema_parameters.get('OTHERNAME', ''))
    configuration.set("SEX", schema_parameters.get('SEX', ''))
    configuration.set("BIRTHDATE", schema_parameters.get('BIRTHDATE', ''))
    configuration.set("IDCARDNO", schema_parameters.get('IDCARDNO', ''))
    configuration.set("PASSPORTNO", schema_parameters.get('PASSPORTNO', ''))
    configuration.set("PASSPORTISSUEDBY", schema_parameters.get('PASSPORTISSUEDBY', ''))
    configuration.set("RESIDENCECOUNTRY", schema_parameters.get('RESIDENCECOUNTRY', ''))
    configuration.set("ORIGINCOUNTRY", schema_parameters.get('ORIGINCOUNTRY', ''))
    configuration.set("OCCUPATION", schema_parameters.get('OCCUPATION', ''))
    configuration.set("COUNTRY", schema_parameters.get('COUNTRY', ''))
    configuration.set("REGION", schema_parameters.get('REGION', ''))
    configuration.set("CITY", schema_parameters.get('CITY', ''))
    configuration.set("SUBCITY", schema_parameters.get('SUBCITY', ''))
    configuration.set("WOREDA", schema_parameters.get('WOREDA', ''))
    configuration.set("HOUSENO", schema_parameters.get('HOUSENO', ''))
    configuration.set("POSTALCODE", schema_parameters.get('POSTALCODE', ''))
    configuration.set("BUSINESSMOBILENO", schema_parameters.get('BUSINESSMOBILENO', ''))
    configuration.set("BUSSINESSTELNO", schema_parameters.get('BUSSINESSTELNO', ''))
    configuration.set("BUSINESSFAXNO", schema_parameters.get('BUSINESSFAXNO', ''))
    configuration.set("RESIDENCETELNO", schema_parameters.get('RESIDENCETELNO', ''))
    configuration.set("EMAILADDRESS", schema_parameters.get('EMAILADDRESS', ''))
    configuration.set("ACCOUNTNO", schema_parameters.get('ACCOUNTNO', ''))
    configuration.set("ACCHOLDERBRANCH", schema_parameters.get('ACCHOLDERBRANCH', ''))
    configuration.set("ACCOWNERNAME", schema_parameters.get('ACCOWNERNAME', ''))
    configuration.set("ACCOUNTTYPE", schema_parameters.get('ACCOUNTTYPE', ''))
    configuration.set("OPENEDDATE", schema_parameters.get('OPENEDDATE', ''))
    configuration.set("BALANCEHELD", schema_parameters.get('BALANCEHELD', ''))
    configuration.set("BALANCEHELDDATE", schema_parameters.get('BALANCEHELDDATE', ''))
    configuration.set("CLOSEDDATE", schema_parameters.get('CLOSEDDATE', ''))
    configuration.set("BENFULLNAME", schema_parameters.get('BENFULLNAME', ''))
    configuration.set("BENACCOUNTNO", schema_parameters.get('BENACCOUNTNO', ''))
    configuration.set("BENBRANCHID", schema_parameters.get('BENBRANCHID', ''))
    configuration.set("BENBRANCHNAME", schema_parameters.get('BENBRANCHNAME', ''))
    configuration.set("BENOWNERENTITY", schema_parameters.get('BENOWNERENTITY', ''))
    configuration.set("BENCOUNTRY", schema_parameters.get('BENCOUNTRY', ''))
    configuration.set("BENREGION", schema_parameters.get('BENREGION', ''))
    configuration.set("BENCITY", schema_parameters.get('BENCITY', ''))
    configuration.set("BENZONE", schema_parameters.get('BENZONE', ''))
    configuration.set("BENWOREDA", schema_parameters.get('BENWOREDA', ''))
    configuration.set("BENHOUSENO", schema_parameters.get('BENHOUSENO', ''))
    configuration.set("BENTELNO", schema_parameters.get('BENTELNO', ''))
    configuration.set("BENISENTITY", schema_parameters.get('BENISENTITY', ''))
    return {
        "message": "success",
        "setting": schema_parameters
    }