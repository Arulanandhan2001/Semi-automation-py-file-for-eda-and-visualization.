def handel(file):
    from pymysql import connect
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import warnings
    warnings.filterwarnings("ignore")
    import pandas as pd

    # connecting the sql data frame to the python.
    
    data=connect(host='localhost',user='root',passwd='123Kaal@#',database='shipper')
    query=f'select * from {file}'
    df=pd.read_sql(query,data)
    data.close()

    # Define conversion rates 
    conversion_rates = {
        'GBP': 1.26704,
        'DKK': 0.143576,
        'EUR': 1.0707,
        'USD': 1.0
    }

    # Update 'salary_in_usd' based on conditions
    df.loc[df['salary_in_usd'].isna(), 'salary_in_usd'] = df.apply(
        lambda row: row['salary'] * conversion_rates.get(row['salary_currency'], np.nan)
        if pd.isna(row['salary_in_usd']) else row['salary_in_usd'], axis=1)
    
    # handiling outliers by using the IQR method. 
    
    def IQR(df,column):
        q1=df[column].quantile(0.15)
        q3=df[column].quantile(0.85)
        iqr=q3-q1
        LW=q1-(1.5*iqr)
        UW=q3+(1.5*iqr)
        df=df[~(df[column]<LW)]
        df=df[~(df[column]>UW)]
        return df
        
    IQR(df,"salary_in_usd")

    # handeling columns for ranking
    
    for i in range(len(df)):
        if df['experience_level'][i]=='EN':   # EN - Entery level
            df['experience_level'][i]=1
        if df['experience_level'][i]=='MI':   # MI - Middle level
            df['experience_level'][i]=2
        if df['experience_level'][i]=='SE':    # SE - sinear level
            df['experience_level'][i]=3
        if df['experience_level'][i]=='EX':    # EX - Experience level
            df['experience_level'][i]=4
        if df["employment_type"][i]=='FT':     # FT - Full time
            df["employment_type"][i]=2
        if df["employment_type"][i]=='PT':     # PT - Part time
            df["employment_type"][i]=1
        if df["employment_type"][i]=='FL':     # FL - Free lance
            df["employment_type"][i]=2
        if df["employment_type"][i]=='CT':     # CT - Not an company employee
            df["employment_type"][i]=2

    # creating the engine to appen the cleaned data frame into the sql data set.
    
    from sqlalchemy import create_engine
    my_conn=create_engine("mysql://root:123Kaal%40#@localhost/shipper")

    try:
        df.to_sql("Cleaned_ML_Salary", con=my_conn, if_exists="replace", index=False)

        print("Table Name : Cleaned_ML_Salary")
    
    except Exception as e:
        print("Error:", e)