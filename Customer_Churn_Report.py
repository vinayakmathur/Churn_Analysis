import pandas as pd
Data = pd.read_excel('C:\\Users\\vinayak.mathur_thero\\Downloads\\Telco_customer_churn.xlsx',sheet_name='Telco_Churn')
#print(Data.head())

churn_by_city = Data[Data['Churn Label']=='Yes'].groupby('City')['Churn Label'].count().sort_values(ascending = False).reset_index()
churn_by_city.columns = ['City','Churn count']
Top_10_Churn_city = churn_by_city.head(10)
#print(Top_10_Churn_city)

import matplotlib.pyplot as plt

plt.figure(figsize =(12,6))
plt.bar(Top_10_Churn_city['City'], Top_10_Churn_city['Churn count'], color='Red')
plt.xticks(rotation=45, ha='right')
plt.title('Top 10 Cities with Highest Customer Churn')
plt.xlabel('City')
plt.ylabel('Churn Count')
plt.tight_layout()
#plt.show()

# Total customers per city
total_customers = Data.groupby('City')['Churn Label'].count().reset_index()
total_customers.columns = ['City', 'Total Customers']

# Churned customers per city
churned_customers = Data[Data['Churn Label'] == 'Yes'].groupby('City')['Churn Label'].count().reset_index()
churned_customers.columns = ['City', 'Churned Customers']

churn_summary = pd.merge(total_customers, churned_customers, on='City', how='left')
churn_summary['Churn Percentage'] = (churn_summary['Churned Customers'] / churn_summary['Total Customers']) * 100

top_10_churn_pct = churn_summary.sort_values(by='Churn Percentage', ascending=True).head(10)

top_10_churn_pct['Churn Percentage'] = top_10_churn_pct['Churn Percentage'].round(2)

#print(top_10_churn_pct)


# Plotting
plt.figure(figsize=(12, 6))
plt.bar(top_10_churn_pct['City'], top_10_churn_pct['Churn Percentage'], color='orange')

plt.xticks(rotation=45, ha='right')
plt.ylabel('Churn Percentage (%)')
plt.xlabel('City')
plt.title('Top 10 Cities by Churn Percentage')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add values on top of bars
for i, v in enumerate(top_10_churn_pct['Churn Percentage']):
    plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')

plt.tight_layout()
#plt.show()

#Churn Customers By Services
def churn_rate_by_service_column(df, column):
    temp = (
        df[df[column] != 'No']  # Exclude customers who don't use the service
        .groupby(column)['Churn Label']
        .value_counts()
        .unstack()
        .fillna(0)
    )
    temp['Churn Rate (%)'] = (temp['Yes'] / (temp['Yes'] + temp['No'])) * 100
    return temp.reset_index()

internet_service_churn = churn_rate_by_service_column(Data, 'Internet Service')
streaming_tv_churn = churn_rate_by_service_column(Data, 'Streaming TV')

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(
    x='Churn Rate (%)',
    y='Internet Service',  # Replace with 'Streaming TV', etc.
    data=internet_service_churn.sort_values(by='Churn Rate (%)', ascending=False),
    palette='viridis'
)

plt.title('Churn Rate by Internet Service Type')
plt.xlabel('Churn Rate (%)')
plt.ylabel('Service Type')
plt.xlim(0, 100)
#plt.show()




#top_10_churn_pct.to_csv('C:\\Users\\vinayak.mathur_thero\\Desktop\\Coding\\top_10_churn_percentage_cities.csv', index=False)
#internet_service_churn.to_csv('C:\\Users\\vinayak.mathur_thero\\Desktop\\Coding\\internet_service_churn_rate.csv', index=False)
#Implementing random forest ML Model for Churn and Non Churn prediction
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

# Load dataset
df = pd.read_excel(
    r"C:\Users\vinayak.mathur_thero\Downloads\Telco_customer_churn.xlsx", 
    sheet_name="Telco_Churn"
)


# Drop customer ID (it's a unique identifier and not useful for prediction)
df.drop('CustomerID', axis=1, inplace=True)

# Convert 'TotalCharges' to numeric (some may be strings or NaN)
df['Total Charges'] = pd.to_numeric(df['Total Charges'], errors='coerce')
df['Total Charges'].fillna(df['Total Charges'].median(), inplace=True)

# Encode the target variable: 'ChurnLabel' (after stripping column names, it's ChurnLabel)
df['Churn Label'] = df['Churn Label'].map({'No': 0, 'Yes': 1})

# Drop known leakage columns — they reveal the outcome
leakage_cols = ['Churn Value', 'Churn Score', 'CLTV', 'Churn Reason']
df.drop(leakage_cols, axis=1, inplace=True)

# Encode all remaining categorical variables using LabelEncoder
le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col].astype(str))

# Define features and target
X = df.drop('Churn Label', axis=1)
y = df['Churn Label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train_scaled, y_train)

# Predict and evaluate
y_pred = rf.predict(X_test_scaled)

#print("Accuracy Score:", accuracy_score(y_test, y_pred))
#print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
#print("\nClassification Report:\n", classification_report(y_test, y_pred))
import matplotlib.pyplot as plt
import seaborn as sns

feat_importances = pd.Series(rf.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.title("Top 10 Features Influencing Churn")
plt.show()
