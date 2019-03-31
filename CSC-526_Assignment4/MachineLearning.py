# Justin Oakley
# CSC-526 Assignment 4: Machine Learning
# 04/01/19

import pandas as pd, sklearn, numpy as np

def print_list(param_list):
    for item in param_list:
        print(item)

# Import cervical cancer data.
cerv_cancer = pd.read_csv("risk_factors_cervical_cancer.csv")
cerv_cancer

# Drop null values from dataframe.
cerv_cancer = cerv_cancer.drop(columns=['STDs: Time since first diagnosis','STDs: Time since last diagnosis'])
cerv_cancer = cerv_cancer.replace(to_replace='?', value=np.nan).dropna()

#Basic statistical analysis
cerv_cancer_mean = [(col, cerv_cancer[col].astype('float64').mean()) for col in cerv_cancer.columns]
print("The mean of each feature:")
print_list(cerv_cancer_mean)
print('\n')
cerv_cancer_std = [(col, cerv_cancer[col].astype('float64').std()) for col in cerv_cancer.columns]
print("The standard deviation of each feature:")
print_list(cerv_cancer_std)
print('\n')

# Drop columns with mean and/or standard deviation values of 0.0
cerv_cancer = cerv_cancer.drop(columns=[mean_item[0] for mean_item, stddev_item in zip(cerv_cancer_mean, cerv_cancer_std)
                                        if mean_item[1] == 0 or stddev_item[1] == 0])

# Split current dataframe to prepare for train_test_split()
X = cerv_cancer.drop(columns=['Dx:Cancer'])
y = cerv_cancer['Dx:Cancer']

# Create training and testing sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=100)

# Standardize datasets for Random Forest Classifier
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Create Random Forest Classifier Model and find the most important features in the dataset.
from sklearn.ensemble import RandomForestClassifier

rf = RandomForestClassifier(n_estimators=100, max_depth=2,random_state=0)
rf_model = rf.fit(X_train, y_train)
feat_importances = [(X.columns[idx], col) for col,idx in zip(rf_model.feature_importances_,
                                                                  range(len(rf_model.feature_importances_)))]
most_important_feats = [feat for feat in feat_importances if feat[1] > 0]

# Print column names with their accuracy scores.
print("\nAll important features in determining cervical cancer:")
print_list(feat_importances)
print('\n')
print("Most important features in determining cervical cancer:")
print_list(most_important_feats)
print('\n')

# Calculate prediction accuracy of Random Forest Model
from sklearn import metrics
predictions = rf_model.predict(X_test)
print("Accuracy of Random Forest Model: %s" % metrics.accuracy_score(y_test, predictions))
