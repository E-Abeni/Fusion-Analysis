import random

class SanctionWatchlistRisk:
    def __init__(self, df, transaction, sanction_list=None, watchlist=None, pep_list=None):
        self.df = df
        self.transaction = transaction
        self.sanction_list = sanction_list or []
        self.watchlist = watchlist or []

    def risk_score_sanctions(self):
        sanction_hit_account =  self.transaction.FULL_NAME in self.sanction_list 
        sanction_hit_ben = self.transaction.BENFULLNAME in self.sanction_list
        return {
            "account_sanction_hit": sanction_hit_account,
            "beneficiary_sanction_hit": sanction_hit_ben,
            "sanction_risk_score": 100 if sanction_hit_account or sanction_hit_ben else 0
        }

    def risk_score_watchlists(self):
        watchlist_hit_account =  self.transaction.FULL_NAME in self.watchlist 
        watchlist_hit_ben = self.transaction.BENFULLNAME in self.watchlist
        return {
            "account_watchlist_hit": watchlist_hit_account,
            "beneficiary_watchlist_hit": watchlist_hit_ben,
            "watchlist_risk_score": 100 if watchlist_hit_account or watchlist_hit_ben else 0
        }

    def risk_score_pep(self):
        pep_hit_account =  self.transaction.FULL_NAME in self.pep_list 
        pep_hit_ben = self.transaction.BENFULLNAME in self.pep_list
        return {
            "account_pep_hit": pep_hit_account,
            "beneficiary_pep_hit": pep_hit_ben,
            "pep_risk_score": 100 if pep_hit_account or pep_hit_ben else 0
        }

    def risk_score_adverse_media(self):
        return random.randint(1, 100)

    def risk_score_regulatory_warnings(self):
        return random.randint(1, 100)

    def detailed_risk_scores(self):
        return {
            "sanctions_risk": self.risk_score_sanctions(),
            "watchlists_risk": self.risk_score_watchlists(),
            "pep_risk": self.risk_score_pep(),
            "adverse_media_risk": self.risk_score_adverse_media(),
            "regulatory_warnings_risk": self.risk_score_regulatory_warnings(),
        }

    def overall_risk_score(self):
        scores = self.detailed_risk_scores()
        return sum(scores.values()) / len(scores)

    def generate_sanction_and_watchlist_risk_report(self):
        detailed_scores = self.detailed_risk_scores()
        overall_risk = sum(detailed_scores.values()) / len(detailed_scores)
        
        return {
            "overall_risk": overall_risk,
            "details": detailed_scores
        }

if __name__ == "__main__":
    risk_calculator = SanctionWatchlistRisk(df=None, transaction=None)
    risk_report = risk_calculator.generate_sanction_and_watchlist_risk_report()
    print(risk_report)

