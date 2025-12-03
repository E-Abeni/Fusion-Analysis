from app.database.database import Base
from sqlalchemy import Column, Integer, String

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    code = Column(String, unique=True, index=True)
    risk_score = Column(Integer)
    
    def __repr__(self):
        return f"<Country(name={self.name}, code={self.code}, risk_score={self.risk_score})>"
