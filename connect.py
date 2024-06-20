def tosql(file):
    from sqlalchemy import create_engine
    import pandas as pd

    ML=pd.read_csv(f'{file}')     # reading the csv file.

    my_conn=create_engine("mysql://root:123Kaal%40#@localhost/shipper")   # creating the engine.

    try:
        ML.to_sql('ML_salary', con=my_conn, if_exists="replace", index=False)      # appending in to the sql.
    
                        # Query to select all data from the table
        query = f"SELECT * FROM {ML}"
        ML_salary = pd.read_sql(query, con=my_conn)
    
                        # Print the retrieved DataFrame
        print(Ml_salary)

    except Exception as e:
        print("Error:", e)