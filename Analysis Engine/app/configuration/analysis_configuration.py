from app.configuration import Configuration

configuration = Configuration ("configuration/kv_store.db")

def get_customer_analysis_settings():
    return {
        'Peer Group Analysis': configuration.get("Peer Group Analysis"),
        'Peer Group Analysis Threshold': configuration.get("Peer Group Analysis Threshold"),
        'Anomaly Detection': configuration.get("Anomaly Detection"),
        'Anomaly Detection Sensitivity': configuration.get("Anomaly Detection Sensitivity"),
        'Time Gap Analysis': configuration.get("Time Gap Analysis"),
        'Time Gap Threshold Seconds': configuration.get("Time Gap Threshold Seconds"),
        'KYC Integrity Check': configuration.get("KYC Integrity Check"),
        'Sanctions List Check': configuration.get("Sanctions List Check"),
        'Watchlist Check': configuration.get("Watchlist Check"),
        'Geographic Risk Assessment': configuration.get("Geographic Risk Assessment")
    }


def set_customer_analysis_settings(analysis_parameters):
    configuration.set("Peer Group Analysis", analysis_parameters.get('Peer Group Analysis', ''))
    configuration.set("Peer Group Analysis Threshold", analysis_parameters.get('Peer Group Analysis Threshold', ''))
    configuration.set("Anomaly Detection", analysis_parameters.get('Anomaly Detection', ''))
    configuration.set("Anomaly Detection Sensitivity", analysis_parameters.get('Anomaly Detection Sensitivity', ''))
    configuration.set("Time Gap Analysis", analysis_parameters.get('Time Gap Analysis', ''))
    configuration.set("Time Gap Threshold Seconds", analysis_parameters.get('Time Gap Threshold Seconds', ''))
    configuration.set("KYC Integrity Check", analysis_parameters.get('KYC Integrity Check', ''))
    configuration.set("Sanctions List Check", analysis_parameters.get('Sanctions List Check', ''))
    configuration.set("Watchlist Check", analysis_parameters.get('Watchlist Check', ''))
    configuration.set("Geographic Risk Assessment", analysis_parameters.get('Geographic Risk Assessment', ''))

    return {
        "message": "success",
        "setting": analysis_parameters
    }