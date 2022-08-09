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
print(home_data.columns) 
features = ['LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr', 'TotRmsAbvGrd']

# Select columns corresponding to features, and preview the data 
X = home_data[features]
print(X.head()) 

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# Define a random forest model and validate with Mean Absolute Error 
# with various values of hyperparameters 
mea_dict = {}
for n in [65, 70, 75, 80]: 
    for d in [12, 15, 18]:
        rf_model = RandomForestRegressor(n_estimators=n, max_depth=d, random_state=1)
        rf_model.fit(train_X, train_y)
        rf_val_predictions = rf_model.predict(val_X)
        rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)
        mea_dict[(n, d)] = rf_val_mae
        out_str = "Validation MAE for RF Model with {} estimators and max depth {}: {:,.0f}"
        print(out_str.format(str(n).rjust(2), str(d).rjust(2), rf_val_mae))
(N, D) = min(mea_dict, key=mea_dict.get)
print("\nMin MAE with {}: {:,.0f}".format((N, D), mea_dict[(N, D)]))

# create a new Random Forest model and fit model on all data 
rf_model_on_full_data = RandomForestRegressor(n_estimators=70, max_depth=15, random_state=1) 
rf_model_on_full_data.fit(X, y)

# predict using test data
test_data_path = 'data/test.csv'
test_data = pd.read_csv(test_data_path)
test_X = test_data[features]
test_preds = rf_model_on_full_data.predict(test_X)
