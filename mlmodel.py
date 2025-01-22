import json
import pandas as pd
import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error 

def nft_pnl(token_data): # calculates overall profit and loss ratio
    nft_pnl= token_data['pnl']['nft_pnl']
    pnl_total=token_data['pnl']['realized_pnl'] + token_data['pnl']['unrealized_pnl']
    pnl_ratio= nft_pnl/ pnl_total
    return(round(pnl_ratio, 2))

def trading_pnl(token_data): # calculates overall profit and loss ratio for trading
    trading_pnl= token_data['pnl']['trading_pnl']
    pnl_total=token_data['pnl']['realized_pnl'] + token_data['pnl']['unrealized_pnl']
    trading_pnl_ratio= trading_pnl / pnl_total
    return(round(trading_pnl_ratio, 3))


def process_json(file_path):
    # Open and load the JSON file
    data_cleaned=[]
    with open(file_path, 'r') as file:
        data = json.load(file)
        for entry in data:
            data_entry=dict()
            entry['pnl']['nft_pnl']/= 1000000 #divide by solana lamport 
            entry['pnl']['trading_pnl']/= 1000000
            entry['pnl']['realized_pnl']/= 1000000
            entry['pnl']['unrealized_pnl']/= 1000000
            entry['total_token_balance']= list(map(lambda x: x / 1000000, entry['total_token_balance']))
            entry['total_sol_balance']= list(map(lambda x: x / 1000000, entry['total_sol_balance']))
            entry['total_nft_balance']= list(map(lambda x: x / 1000000, entry['total_nft_balance']))
            data_entry['date_wallet_created']=  datetime.datetime.utcfromtimestamp(entry['wallet_genesis']).strftime('%Y-%m-%d')  #address
            data_entry['address']= entry['address'] #address
 
            data_entry['trading_pnl']= entry['pnl']['trading_pnl'] #get trading pnl

            data_entry['nft_pnl']= entry['pnl']['nft_pnl'] #get nft pnl

            data_entry['nft_pl_ratio']=  nft_pnl(entry)  #calculate nft pnl ratio
            data_entry['nft_winrate']=  entry['nft_winrate'][0]/entry['nft_winrate'][1] #calculate nft win rate

            data_entry['trading_pnl_ratio']= trading_pnl(entry) #calculate trading pnl ratio
            data_entry['trade_winrate']=  entry['trade_winrate'][0]/entry['trade_winrate'][1] #calculate nft win rate
            data_entry['liquidity_ratio']=  round(entry['number_of_active_trades']/entry['total_number_of_trades'],2) #calculate liquidity ratio
            data_entry['trading_frequency']= round(entry['number_of_active_trades']/entry['total_number_of_trades'],2) #calculate trading frequency
            data_entry['nft_sales_rate']= round(entry['number_of_nft_sales']/entry['total_number_of_nft_trades'],2) #calculate nft sales rate
            data_entry['prop_success_trades']= round(entry['number_of_closed_trades']/entry['total_number_of_trades'] * data_entry['trade_winrate'],2) #calculate proportion of success rate
        

            data_cleaned.append(data_entry)

    return pd.DataFrame(data_cleaned)

data= process_json("exampleData.json")[['nft_pl_ratio', 'trading_pnl_ratio', 'liquidity_ratio', 'trading_frequency', 
 'nft_sales_rate', 'trading_pnl']] #select variables for model 

X= data.drop(columns=['trading_pnl'])  # Assuming 'trading_pnl' is the target
y = data['trading_pnl']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Regressor
rf = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
rf.fit(X_train, y_train)

# Make predictions
y_pred = rf.predict(X_test)

# Evaluate the model
mse = mean_squared_error(y_test, y_pred)

import pickle
pickle_out= open("model.pkl", "wb")
pickle.dump(rf, pickle_out)
pickle_out.close()

##### example prediciton

# example_obs= {
#     'nft_pl_ratio': 0.8,
#     'trading_pnl_ratio':  0.7,
#     'liquidity_ratio': 0.6,
#     'trading_frequency': 1.2,
#     'nft_sales_rate': -0.3
# }
# feature_order = ['nft_pl_ratio', 'trading_pnl_ratio', 'liquidity_ratio', 'trading_frequency', 'nft_sales_rate']

# # Convert dictionary to a properly ordered NumPy array
# ordered_values = [example_obs[feature] for feature in feature_order]
# new_observation = np.array(ordered_values).reshape(1, -1)  # Shape (1, num_features)


# # Make prediction
# prediction = rf.predict(new_observation)
# print("Your Expected Profit and Loss Trade:", prediction[0])
