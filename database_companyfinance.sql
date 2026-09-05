CREATE DATABASE CompanyFinance;
USE CompanyFinance;

-- Tabell som innehåller information angående transaktioner.
CREATE TABLE transactions (
    transaction_id VARCHAR(50),
    transaction_date DATETIME,
    department VARCHAR(50),
    category VARCHAR(50),
    region VARCHAR(50),
    payment_method VARCHAR(50),
    PRIMARY KEY (transaction_id)
);

-- Tabell som innnehåller budget och faktiskt spendering.
CREATE TABLE financial_amounts (
	transaction_id VARCHAR(50),
    budget_amount DECIMAL(15,2),
    actual_amount DECIMAL(15,2),
    PRIMARY KEY (transaction_id),
    FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    );


	
-- Beräkning av budget, utfall samt avvikelser.
SELECT t.department AS Department,
SUM(f.budget_amount) AS Total_Budget,
SUM(f.actual_amount) AS Total_Actual,
-- Avvikelse i kr
SUM(f.budget_amount) - SUM(f.actual_amount) AS Variance,
-- Avvikelse i procent
ROUND((SUM(f.actual_amount) - SUM(f.budget_amount)) / SUM(f.budget_amount) * 100,2) AS Variance_Procent

FROM  transactions AS t

INNER JOIN financial_amounts AS f
ON t.transaction_id = f.transaction_id

GROUP BY t.department;
