# Housing Prices Competition 
# on Kaggle 
#
# https://www.kaggle.com/code/samsonblack/exercise-machine-learning-competitions?scriptVersionId=98048459 

# Import libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

# Load the data, and separate the target
iowa_file_path = 'data/train.csv'
home_data = pd.read_csv(iowa_file_path)
y = home_data.SalePrice

# Select important features 
# print(home_data.columns) 
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']

# Select columns corresponding to features, and preview the data 
X = home_data[features]
print(X.head()) 

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Define a random forest model and validate with Mean Absolute Error 
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(train_X, train_y)
rf_val_predictions = rf_model.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)
out_str = 'Mean Absolute Error with for Random Forest Model:  {:,.0f}'
print(out_str.format(rf_val_mae)) 

print('\n') 
print(dir(rf_model))
print('\n') 

param_dict = rf_model.get_params()
print(param_dict) 


# create a new Random Forest model and fit model on all data 
rf_model_on_full_data = RandomForestRegressor(random_state=1) 
rf_model_on_full_data.fit(X, y)

# predict using test data
test_data_path = 'data/test.csv'
test_data = pd.read_csv(test_data_path)
test_X = test_data[features]
test_preds = rf_model_on_full_data.predict(test_X)

# save predictions as CSV 
output = pd.DataFrame({'Id': test_data.Id,
                       'SalePrice': test_preds})
output.to_csv('data/submission.csv', index=False)