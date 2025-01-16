import json
import pandas as pd
file_path= "exampleData.json"


# Open and load the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

df= data['holdings']

tokens_df = pd.DataFrame( # dataframe that describes current wallet holdings
    [{
        'token': item['token'], 
        'balance': item['balance'], 
        'value_usd': item['value_usd']
    } for item in df]
)

recent_trades = [] #dataframe that has recent trades
for item in df:
    for trade in item['recent_trades']:
        trade_data = {
            'token': item['token'], 
            'type': trade['type'], 
            'price': trade['price'], 
            'timestamp': trade['timestamp']
        }
        recent_trades.append(trade_data)

trades_df = pd.DataFrame(recent_trades)


print("Tokens Overview:")
print(tokens_df)

print("\nRecent Trades:")
print(trades_df)

print(df)