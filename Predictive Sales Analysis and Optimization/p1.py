import pandas as pd

customers = pd.read_csv('customers.csv')
products = pd.read_csv('products.csv')
sales = pd.read_csv('sales.csv')
returns = pd.read_csv('returns.csv')

print(customers.isnull().sum())

customers.dropna(subset=['Name', 'Email'])

customers['Age'].fillna(customers['Age'].median())

customers['Gender'].fillna(customers['Gender'].mode()[0])
customers['Region'].fillna(customers['Region'].mode()[0])

customers.drop_duplicates(subset=['CustomerID'])


print(products.isnull().sum())

products['Price'].fillna(products['Price'].median())

products['ProductName'].fillna('Unknown Product')

products['StockQuantity'].fillna(products['StockQuantity'].mean())

products['Category'].fillna(products['Category'].mode()[0])

products.drop_duplicates(subset=['ProductID'])

print(returns.isnull().sum())

returns.dropna(subset=['SaleID'])

returns['ReturnDate'].fillna('Unknown')

returns['Reason'].fillna('Unknown Reason')

print(sales.isnull().sum())

sales['Quantity'].fillna(sales['Quantity'].median())
sales['TotalAmount'].fillna(sales['TotalAmount'].median())

sales.drop_duplicates(subset=['SaleID'])

salesCustomers = pd.merge(sales, customers, on='CustomerID', how='inner')

salesCustomersProducts = pd.merge(salesCustomers, products, on='ProductID', how='inner')

finalDf = pd.merge(salesCustomersProducts, returns, on='SaleID', how='left') 

productSales = salesCustomersProducts.groupby('ProductName').agg({'TotalAmount': 'sum'}).reset_index()
topProducts = productSales.sort_values('TotalAmount', ascending=False).head(10)

customerSpending = salesCustomers.groupby('CustomerID').agg({'TotalAmount': 'sum'}).reset_index()
customerSpending['SpendingCategory'] = pd.qcut(customerSpending['TotalAmount'], q=3, labels=['Low', 'Medium', 'High'])

finalDf.to_csv('finalDf.csv', index=False)

import psycopg2
import pandas as pd

# Database connection parameters
db_params = {
    "dbname": "salesAnalysis",
    "user": "postgres",
    "password": "Tushar@4045",
    "host": "localhost",
    "port": 5432
}

# Connect to PostgreSQL
conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

# Function to load a CSV into a PostgreSQL table
def load_csv_to_table(csv_file, table_name, conn, cursor):
    df = pd.read_csv(csv_file)
    # Write DataFrame to PostgreSQL table
    for index, row in df.iterrows():
        placeholders = ', '.join(['%s'] * len(row))
        columns = ', '.join(row.index)
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()

# Load each CSV into its corresponding table
load_csv_to_table('customers.csv', 'customers', conn, cursor)
load_csv_to_table('products.csv', 'products', conn, cursor)
load_csv_to_table('sales.csv', 'sales', conn, cursor)
load_csv_to_table('returns.csv', 'returns', conn, cursor)

# Close the connection
cursor.close()
conn.close()
