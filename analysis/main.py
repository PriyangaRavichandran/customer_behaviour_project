import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize Firebase Admin
cred = credentials.Certificate('../firebase_key.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Load CSV data
df = pd.read_csv('../data/customer_purchases.csv')

# Upload data to Firestore
for _, row in df.iterrows():
    doc_ref = db.collection('purchases').document()
    doc_ref.set(row.to_dict())

print("Data uploaded to Firestore successfully.")

# Analysis 1: Total Spend per Customer
spend_per_customer = df.groupby('CustomerID')['Amount'].sum()
spend_per_customer.plot(kind='bar', title='Total Spend per Customer')
plt.xlabel('Customer ID')
plt.ylabel('Amount')
plt.tight_layout()
plt.savefig('../data/spending_chart.png')
plt.clf()

# Analysis 2: Top Products
top_products = df['Product'].value_counts().nlargest(5)
sns.barplot(x=top_products.values, y=top_products.index)
plt.title('Top 5 Products Purchased')
plt.xlabel('Count')
plt.tight_layout()
plt.savefig('../data/top_products.png')
plt.clf()

# Analysis 3: Monthly Sales
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['Amount'].sum()
monthly_sales.plot(marker='o', title='Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales Amount')
plt.tight_layout()
plt.savefig('../data/monthly_sales.png')
plt.clf()

# Export summary to Excel
summary = pd.DataFrame({
    'Customer': spend_per_customer.index,
    'Total Spent': spend_per_customer.values
})
summary.to_excel('../data/customer_analysis_report.xlsx', index=False)

print("Analysis complete. Reports and charts saved in 'data/' folder.")