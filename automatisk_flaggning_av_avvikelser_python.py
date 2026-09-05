import pandas as pd
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://username:password@localhost/CompanyFinance')

#Kör SQL-query via pandas
query = """
SELECT t.department AS department, SUM(f.budget_amount) AS budget, SUM(f.actual_amount) AS actual
FROM transactions AS t

INNER JOIN financial_amounts AS f
ON t.transaction_id = f.transaction_id
GROUP BY t.department

"""

df_analysis = pd.read_sql(query, con = engine)

#Beräkning av avvikelser i Pandas
df_analysis['Variance_kr'] = df_analysis['budget'] - df_analysis['actual']
df_analysis['Variance_Procent'] = ((df_analysis['actual'] - df_analysis['budget'])/ df_analysis['budget']) * 100

#Hitta avdelningar som har en avvikelse över 10 % över budget
critical_departments = df_analysis[df_analysis['Variance_Procent'] > 10]

#Exportera dessa avvikelser till en Excel-fil
critical_departments.to_excel('Kritiska_Budgetavvikelser.xlsx', index = False)
print("Rapporten har laddats upp i en Excel-fil!")