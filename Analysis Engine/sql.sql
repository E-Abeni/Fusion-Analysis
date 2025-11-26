-- SQLite
--SELECT DISTINCT count(ACCOUNTNO) as number_of_accounts FROM transactions;

--SELECT * FROM transactions;

SELECT count( DISTINCT BENACCOUNTNO) as number_of_recipients FROM transactions;
