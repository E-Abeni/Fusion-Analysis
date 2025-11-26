API End Points
    Live
        - Total Aggregation of transactions in the db
        - Message Queue: Number of messages in the kafka topic
        - Transaction Processing Speed
        - Total Active Alerts
        - Total Transaction volume in 1 minute or 5 minute
        - Total Volume of transaction which are categorized as risky (High and Critical) in 1 minute or 5 minute
        - Alert Trigger distributions
        - Top 5 or 10 Risky Transactions
        - Top 5 or 10 Destinations from all the Risky Transactions
        - Generate STR alerts


    Batch
    - Customer Associated Risk (name, account_number, location)
        * Peer group by occupation and location
        * KYC data integrity results (completness, uniquness, identity verfied (national id), correctness (age, expiry date))
        * Sanction and Watchlist match


Configurations
     - Central Database url, port, username, password
     - Kafka url, topic
     - Update duration for websocket connections
     - Each analysis method
        * Turn on or off
        * Set threshold when necessary
    - Engine Database
        - Sanction lists table
        - Watch lists table
        - High risk countries database
    - Schema match


1. Setup database and kafka

2. Correct data model to store the risk assessment

3. Wireup the analysis


4. Finish and Test the api end points



