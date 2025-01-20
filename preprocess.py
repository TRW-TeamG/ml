import json
import pandas as pd
import datetime

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

# Example usage
data= process_json("exampleData.json")

# print(data)


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# Select numeric columns for clustering
numeric_data = data.select_dtypes(include=['float64'])

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(numeric_data)

# Perform k-means clustering
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(scaled_data)

# Add the cluster labels to the original DataFrame
data['Cluster'] = clusters

# Plotting the first two features with clusters
plt.figure(figsize=(8, 6))
plt.scatter(scaled_data[:, 0], scaled_data[:, 1], c=clusters, cmap='viridis', s=50)
# plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=200, label='Centroids')
plt.title('K-Means Clustering')
plt.xlabel('Feature 1 (Standardized)')
plt.ylabel('Feature 2 (Standardized)')
plt.legend()
plt.show()

# base_prompt = f"""
# Data:

# {data}

# Here's the dataset that I provided. Each entry is a wallet's performance. It shows the trading and NFT profit and loss ratios, 
# win rates, liquidity ratio, trading frequency, NFT sales rate, and proportion of successful trades. 
# Analyze the dataset and recommend me trading strategies based on the data.
# """

# print(base_prompt)
# output_file = "output_data.csv"
# df.to_csv(output_file, index=False)
