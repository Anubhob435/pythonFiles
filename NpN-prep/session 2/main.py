
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the dataset
try:
    data = pd.read_csv('employees_data.csv')
except FileNotFoundError:
    print("Error: 'employees_data.csv' not found. Make sure the file is in the correct directory.")
    exit()

# Drop unnecessary columns
data = data.drop(['EmployeeID', 'FullName', 'HireDate'], axis=1)

# Handle categorical variables
categorical_cols = ['Department', 'JobTitle', 'OfficeLocation']
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])

# Define features (X) and target (y)
X = data.drop('PerformanceRating', axis=1)
y = data['PerformanceRating']

# Initialize the RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Perform cross-validation
# Using cv=5, but you can adjust this based on the dataset size.
# For small datasets, a smaller number of folds might be necessary.
# The number of folds cannot be greater than the number of samples in the smallest class.
cv_scores = cross_val_score(model, X, y, cv=3) # Reduced to 3 folds due to small class sizes

# Print the cross-validation results
print(f"Cross-Validation Scores: {cv_scores}")
print(f"Average CV Score: {np.mean(cv_scores):.2f}")

# To show feature importances, we still need to train the model on the full dataset
model.fit(X, y)

# Feature Importance
print("\nFeature Importances:\n")
feature_importances = pd.DataFrame(model.feature_importances_,
                                   index = X.columns,
                                   columns=['importance']).sort_values('importance', ascending=False)
print(feature_importances)

# Visualize Feature Importances
plt.figure(figsize=(10, 6))
plt.title('Feature Importances')
plt.bar(feature_importances.index, feature_importances['importance'])
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('feature_importances.png')
print("\nFeature importance visualization saved as 'feature_importances.png'")
