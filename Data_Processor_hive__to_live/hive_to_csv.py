from pyhive import hive
import pandas as pd

def main():
    host = "172.20.137.129"  
    port = 10000
    database = "bankdb"
    table = "individual_transactions"


    conn = hive.Connection(host=host, port=port, database=database)
    cursor = conn.cursor()

    size_per_file = 500000

    offset = 0 

    results = [1]

    while len(results) > 0:

        print(f"[Hive To CSV] Running query ..... offset={offset}, size_per_file={size_per_file}")
        query = f"SELECT * FROM {table} LIMIT " + str(size_per_file) + " OFFSET " + str(offset)
        cursor.execute(query)
        results = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        print(f"[Hive To CSV] converting to df.... size={len(results)}")
        df = pd.DataFrame(results, columns=columns)
        df.to_csv(f"transactions_offset_{offset}_size_{len(results)}.csv", index=False)

        offset = offset + size_per_file


    cursor.close()
    conn.close()
    df.head(10)


if __name__ == "__main__":
    main()
