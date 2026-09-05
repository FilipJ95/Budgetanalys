import pandas as pd

from sqlalchemy import create_engine

#Läser in datan
df = pd.read_excel("Budget_vs_Actual_Data.xlsx")

#Omvandlar datum till rätt format 
df['Date'] = pd.to_datetime(df['Date'])

df = df.dropna(subset = ['Transaction ID'])#Rensar rader utan ID
df = df.drop_duplicates(subset=['Transaction ID'])#Rensar dubletter

#Delar upp datan i två tabeller och matchar MySQL struktur
#Tabell 1:  
df_transactions = df[['Transaction ID', 'Date', 'Department', 'Category', 'Region', 'Payment Method']].copy()
df_transactions.columns = ['transaction_id', 'transaction_date', 'department', 'category', 'region', 'payment_method']

#Tabell 2
df_amounts = df[['Transaction ID','Budget Amount','Actual Amount']].copy()
df_amounts.columns = ['transaction_id', 'budget_amount', 'actual_amount']


engine = create_engine('mysql+mysqlconnector://username:password@localhost/CompanyFinance')

#Laddar upp datan till mina tabeller i MySQL
df_transactions.to_sql(
    name="transactions",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000,
)

df_amounts.to_sql(
    name="financial_amounts",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000,
)

print("Data har tvättats och överförts till MySQL!")
