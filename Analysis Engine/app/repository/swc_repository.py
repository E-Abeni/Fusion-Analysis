from app.model.sanction_list import SanctionListEntry
from app.model.watch_list import WatchListEntry
from app.model.countries import Country
from app.database.database import get_engine
from sqlalchemy.orm import Session
import pandas as pd

engine = get_engine()

def get_all_sanction_list_entries(pandas_df=False):
    with Session(engine) as session:
        entries = session.query(SanctionListEntry.FirstName, 
                                SanctionListEntry.LastName).all()
    if pandas_df:
        data = [rp.__dict__ for rp in entries]
        df = pd.DataFrame(data, columns=["FirstName", "LastName"])   
        return df
    return entries

def get_all_watch_list_entries(pandas_df=False):
    with Session(engine) as session:
        entries = session.query(WatchListEntry.FirstName,
                                WatchListEntry.LastName).all()
    if pandas_df:
        data = [rp.__dict__ for rp in entries]
        df = pd.DataFrame(data, columns=["FirstName", "LastName"])   
        return df
    return entries


def insert_sanction_list_entry(entry):
    with Session(engine) as session:
        session.add(entry)
        session.commit()   

def insert_watch_list_entry(entry):
    with Session(engine) as session:
        session.add(entry)
        session.commit()

def delete_sanction_list_entry(entry_id):
    with Session(engine) as session:
        entry = session.query(SanctionListEntry).filter(SanctionListEntry.id == entry_id).first()
        if entry:
            session.delete(entry)
            session.commit()


def delete_watch_list_entry(entry_id):
    with Session(engine) as session:
        entry = session.query(WatchListEntry).filter(WatchListEntry.id == entry_id).first()
        if entry:
            session.delete(entry)
            session.commit()   


def update_sanction_list_entry(entry):
    with Session(engine) as session:
        existing_entry = session.query(SanctionListEntry).filter(SanctionListEntry.id == entry.id).first()
        if existing_entry:
            for key, value in entry.__dict__.items():
                setattr(existing_entry, key, value)
            session.commit()


def update_watch_list_entry(entry):
    with Session(engine) as session:
        existing_entry = session.query(WatchListEntry).filter(WatchListEntry.id == entry.id).first()
        if existing_entry:
            for key, value in entry.__dict__.items():
                setattr(existing_entry, key, value)
            session.commit()





def get_all_countries(pandas_df=False):
    with Session(engine) as session:
        countries = session.query(Country.name, Country.risk_score).all()
    if pandas_df:
        data = [rp.__dict__ for rp in countries]
        df = pd.DataFrame(data, columns=["name", "risk_score"])   
        return df
    return countries

def insert_country(country):
    with Session(engine) as session:
        session.add(country)
        session.commit()

def delete_country(country_id):
    with Session(engine) as session:
        country = session.query(Country).filter(Country.id == country_id).first()
        if country:
            session.delete(country)
            session.commit()

def update_country(country):
    with Session(engine) as session:
        existing_country = session.query(Country).filter(Country.id == country.id).first()
        if existing_country:
            for key, value in country.__dict__.items():
                setattr(existing_country, key, value)
            session.commit()

def get_country_by_name(name):
    with Session(engine) as session:
        country = session.query(Country).filter(Country.name == name).first()
    return country


if __name__ == "__main__":
    countries = get_all_countries()
    for country in countries:
        print(country)



