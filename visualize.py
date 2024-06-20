def vis(file):
    from pymysql import connect
    import matplotlib.pyplot as plt
    import seaborn as sns
    import plotly.express as px
    import plotly.graph_objects as go
    import warnings
    warnings.filterwarnings("ignore")
    import pandas as pd
    data=connect(host="localhost",user="root",password="123Kaal@#",database="shipper")
    query=f"select * from {file}"
    df=pd.read_sql(query,data)
    data.close()

    # Bar Plot for Salary by Year and Company Size

    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='work_year', y='salary_in_usd', hue='company_size', ci=None)
    plt.title('Average Salary by Year and Company Size')
    plt.xlabel('Work Year')
    plt.ylabel('Average Salary in USD')
    plt.legend(title='Company Size')
    plt.show()
    
    # Segmented bi-variate analysis.

    fig = px.histogram(df, x='salary_in_usd', nbins=50, color='job_title', title='Distribution of salary and job')
    fig.show()

   # Heatmap for Salary Correlation

    correlation_matrix = df[['employment_type','experience_level','salary_in_usd', 'remote_ratio', 'work_year']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='YlGnBu', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap for Salary, Remote Ratio, and Work Year')
    plt.show()

    # Scatter Plot for Salary vs. Remote Ratio, Colored by Company Size
    fig = px.scatter(df, x='remote_ratio', y='salary_in_usd', color='company_size',
                 title='Salary vs. Remote Ratio by Company Size',
                 labels={'remote_ratio': 'Remote Ratio', 'salary_in_usd': 'Salary in USD'},
                 hover_data=['work_year', 'company_location'])
    fig.show()

    #Pie chart for distribution of company sizes

    company_size_counts = df['company_size'].value_counts()
    plt.figure(figsize=(8, 8))
    plt.pie(company_size_counts, labels=company_size_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
    plt.title('Distribution of Company Sizes')
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()

    # Multivariate analysis

    fig = px.scatter_3d(df, x='company_size', y='salary_in_usd', z='job_title', color='salary_in_usd', title='Price vs. Square Footage of Living Area and Bedrooms')
    fig.show()

    # Interactive scatter plot
    fig = px.scatter(
        df,
        x='company_location',
        y='salary_in_usd',
        color='company_location',
        size='salary_in_usd',
        hover_data=['work_year', 'remote_ratio', 'company_size'],
        title='Salary in USD by Company Location',
        labels={
            'company_location': 'Company Location',
            'salary_in_usd': 'Salary in USD'
        }
    )

    # Show the plot
    fig.show()