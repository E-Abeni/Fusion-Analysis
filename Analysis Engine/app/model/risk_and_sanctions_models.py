from dataclasses import dataclass
from typing import Optional, List, Any


@dataclass
class CustomerRiskProfile:
    """
    Represents the calculated risk profile for a customer based on internal models.
    This data is crucial for determining the frequency and depth of due diligence (CDD/EDD).
    """
    CUSTOMERID: int             # Primary key / Foreign key linking to the main Customer table
    ACCOUNTNO: str              # The account number associated with the customer
    DEMOGRAPHICS_RISK: float    # Risk score based on demographic factors
    CUSTOMER_TYPE_RISK: float   # Risk score based on customer type (e.g., individual, corporate, high-net-worth)
    TRANSACTION_HISTORY_RISK: float # Risk score based on historical transaction patterns
    RISKSCORE: float            # The numerical risk score (e.g., 0.0 to 100.0)
    RISKLEVEL: str              # Categorical risk level ('Low', 'Medium', 'High', 'Elevated')
    REVIEWFREQUENCY_DAYS: int   # How often (in days) the risk profile must be reassessed
    LASTREVIEWDATE: str         # The date of the last risk assessment
    NEXTREVIEWDATE: str         # The scheduled date for the next review
    REASONCODES_JSON: str       # JSON string listing specific factors contributing to the score (e.g., ['high_cash_vol', 'pep_relative'])
    STATUS: str                 # Status of the profile ('Active', 'On Hold', 'De-risked')
    CREATED_AT: str
    UPDATED_AT: str

    @classmethod
    def from_db_row(cls, row: tuple) -> 'CustomerRiskProfile':
        """Converts a tuple of row data into a CustomerRiskProfile dataclass instance."""
        return cls(*row)


@dataclass
class SanctionWatchlistRiskProfile:
    """
    Represents the risk profile related to sanctions and watchlists for a customer.
    This profile helps in identifying potential compliance issues.
    """
    SANCTIONWATCHLISTHITID: int # Primary key
    CUSTOMERID: int             # Primary key / Foreign key linking to the main Customer table
    ACCOUNTNO: str              # The account number associated with the customer
    SANCTIONS_RISK: float       # Risk score based on sanctions list hits
    WATCHLIST_RISK: float       # Risk score based on watchlist hits (PEP, Adverse Media)
    PEP_RISK: float             # Risk score based on Politically Exposed Persons (PEP) hits
    ADVERSE_MEDIA_RISK: float   # Risk score based on adverse media hits
    REGULATORY_WARNINGS_RISK: float # Risk score based on regulatory warnings
    OVERALL_RISK_SCORE: float   # Combined overall risk score
    RISKLEVEL: str              # Categorical risk level ('Low', 'Medium', 'High', 'Elevated')
    LASTSCREENEDDATE: str       # The date of the last sanctions/watchlist screening
    NEXTSCREENINGDATE: str      # The scheduled date for the next screening
    REVIEWFREQUENCY_DAYS: int   # How often (in days) the screening must be performed
    STATUS: str                 # Status of the profile ('Active', 'On Hold', 'Cleared')
    CREATED_AT: str
    UPDATED_AT: str

    @classmethod
    def from_db_row(cls, row: tuple) -> 'SanctionWatchlistRiskProfile':
        """Converts a tuple of row data into a SanctionWatchlistRiskProfile dataclass instance."""
        return cls(*row)




'''
# --- 2. Sanction Hit Model ---

@dataclass
class SanctionHit:
    """
    Records a potential match against a governmental/international sanctions list (e.g., OFAC, UN, EU).
    These hits typically require immediate freezing of funds and detailed manual review.
    """
    SANCTIONHITID: int          # Primary Key
    CUSTOMERID: int             # Foreign key to the Customer
    TRANSACTIONID: Optional[int]# Optional: Link to the transaction that triggered the screening
    LISTNAME: str               # The specific sanctions list hit (e.g., 'OFAC_SDN', 'UNSC')
    MATCHSCORE: int             # The confidence score of the match (0-100)
    MATCHTYPE: str              # The field that matched (e.g., 'Name Match', 'Passport Match', 'Alias Match')
    SANCTIONENTITYID: str       # The ID of the matched entity on the source list
    SANCTIONENTITYDETAILS_JSON: str # JSON string containing the full details of the sanctioned entity
    SCREENDATE: str             # Date and time the screening was performed
    REVIEWERID: Optional[str]   # User ID of the analyst who reviewed the hit
    DISPOSITION: str            # Final resolution ('False Positive', 'Confirmed Hit', 'Escalated', 'Pending')

    @classmethod
    def from_db_row(cls, row: tuple) -> 'SanctionHit':
        """Converts a tuple of row data into a SanctionHit dataclass instance."""
        return cls(*row)


# --- 3. Watchlist Hit Model (PEP & Adverse Media) ---

@dataclass
class WatchlistHit:
    """
    Records a potential match against broader watchlists, such as Politically Exposed Persons (PEPs)
    or Adverse Media lists. These often trigger Enhanced Due Diligence (EDD).
    """
    WATCHLISTHITID: int         # Primary Key
    CUSTOMERID: int             # Foreign key to the Customer
    WATCHLISTTYPE: str          # Type of watchlist ('PEP', 'Adverse Media', 'Regulatory Warning')
    LISTPROVIDER: str           # The service or source that provided the list data
    MATCHSCORE: int             # The confidence score of the match (0-100)
    ENTITYREFERENCE: str        # Reference ID of the entity on the provider's system
    ENTITYCOUNTRY: Optional[str]# Country associated with the PEP/Media entity
    SCREENDATE: str             # Date and time the screening was performed
    REVIEWERID: Optional[str]
    DISPOSITION: str            # Final resolution ('False Positive', 'Confirmed Match - EDD Initiated', 'Closed')
    REVIEW_NOTES: Optional[str] # Analyst notes regarding the decision

    @classmethod
    def from_db_row(cls, row: tuple) -> 'WatchlistHit':
        """Converts a tuple of row data into a WatchlistHit dataclass instance."""
        return cls(*row)

'''