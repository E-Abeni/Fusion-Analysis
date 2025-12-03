from app.model.transaction_risk_profile import TransactionRiskProfile
from sqlalchemy.orm import Session
from app.database.database import get_engine
import pandas as pd

engine = get_engine()

def get_all_transaction_risk_profiles():
    with Session(engine) as session:
        risk_profiles = session.query(TransactionRiskProfile).all()
    return risk_profiles

def get_all_transaction_risk_profiles_pandas_df():
    risk_profiles = get_all_transaction_risk_profiles()
    data = [rp.__dict__ for rp in risk_profiles]
    df = pd.DataFrame(data)
    return df


def get_transaction_risk_profile_by_id(risk_profile_id):
    with Session(engine) as session:
        risk_profile = session.query(TransactionRiskProfile).filter(TransactionRiskProfile.RISKPROFILEID == risk_profile_id).first()
    return risk_profile

def insert_transaction_risk_profile(risk_profile):
    with Session(engine) as session:
        session.add(risk_profile)
        session.commit()

def update_transaction_risk_profile(risk_profile):
    with Session(engine) as session:
        existing_risk_profile = session.query(TransactionRiskProfile).filter(TransactionRiskProfile.RISKPROFILEID == risk_profile.RISKPROFILEID).first()
        if existing_risk_profile:
            for key, value in risk_profile.__dict__.items():
                setattr(existing_risk_profile, key, value)
            session.commit()

def delete_transaction_risk_profile(risk_profile_id):
    with Session(engine) as session:
        risk_profile = session.query(TransactionRiskProfile).filter(TransactionRiskProfile.RISKPROFILEID == risk_profile_id).first()
        if risk_profile:
            session.delete(risk_profile)
            session.commit()

def insert_transaction_risk_profiles_bulk(risk_profiles):
    with Session(engine) as session:
        session.bulk_save_objects(risk_profiles)
        session.commit()

def get_transaction_risk_profiles_by_customer(customer_id):
    with Session(engine) as session:
        risk_profiles = session.query(TransactionRiskProfile).filter(TransactionRiskProfile.CUSTOMERID == customer_id).all()
    return risk_profiles

def get_transaction_risk_profiles_by_risk_level(risk_level):
    with Session(engine) as session:
        risk_profiles = session.query(TransactionRiskProfile).filter(TransactionRiskProfile.RISKLEVEL == risk_level).all()
    return risk_profiles

def get_transaction_risk_profiles_by_date_range(start_date, end_date):
    with Session(engine) as session:
        risk_profiles = session.query(TransactionRiskProfile).filter(
            TransactionRiskProfile.ASSESSMENTDATE >= start_date,
            TransactionRiskProfile.ASSESSMENTDATE <= end_date
        ).all()
    return risk_profiles


if __name__ == "__main__":
    df = get_all_transaction_risk_profiles_pandas_df()
    print(df.head())
