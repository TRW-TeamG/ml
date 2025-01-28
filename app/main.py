import uvicorn
from fastapi import FastAPI
from typing import Dict
import uvicorn
import pickle
import numpy as np 
from pydantic import BaseModel
import google.generativeai as genai
from gmgn import gmgn
import requests
import pandas as pd
from dotenv import load_dotenv
import os
load_dotenv()

model = pickle.load(open("model.pkl", "rb") )
anomaly_model= pickle.load(open("anomaly_model.pkl", "rb"))

################### FUNCTIONC CALLING FUNCTIONS #################

def predict_wallet_pnl(nft_pl_ratio:float, trading_pnl_ratio:float, #this function calls the model to predict the pnl of a wallet. 
                        liquidity_ratio:float, trading_frequency:float,  #The LLM will reference this function (predict_wallet_pnl) to calculate PNL from user prompt
                          nft_sales_rate:float):
    
    """"
    Predicts the PNL (profit and loss) of a wallet based on wallet statistics.

    Args:
        nft_pl_ratio (float): The ratio of NFT (non fungible token) PNL.
        trading_pnl_ratio (float): The ratio of trading PNL.
        liquidity_ratio (float): The liquidity ratio.
        trading_frequency (float): The trading frequency.
        nft_sales_rate (float): The NFT sales rate.

    Returns:
        float: The predicted PNL of the wallet.
    
    
    """
    input_data = np.array([[nft_pl_ratio, trading_pnl_ratio, 
                   liquidity_ratio, trading_frequency, nft_sales_rate]])
    

    prediction = model.predict(input_data)


    return float(prediction[0])


def fetch_wallet_data(wallets): #takes a dictionary of wallets and returns a dictionary
    extracted_data = []
    for wallet in wallets:
        data = {
            "symbol": wallet.get("name"),
            "holder_count": wallet.get("holder_count"),
            "price": wallet.get("price"),
            "liquidity": wallet.get("liquidity"),
            "volume_24h": wallet.get("volume_24h"),
            "volume_6h": wallet.get("volume_6h"),
            "volume_1h": wallet.get("volume_1h"),
            "volume_5m": wallet.get("volume_5m"),
            "volume_1m": wallet.get("volume_1m"),
            "swaps_24h": wallet.get("swaps_24h"),
            "swaps_6h": wallet.get("swaps_6h"),
            "swaps_1h": wallet.get("swaps_1h"),
            "swaps_5m": wallet.get("swaps_5m"),
            "swaps_1m": wallet.get("swaps_1m"),
            "net_in_volume_24h": wallet.get("net_in_volume_24h"),
            "net_in_volume_6h": wallet.get("net_in_volume_6h"),
            "net_in_volume_1h": wallet.get("net_in_volume_1h"),
            "net_in_volume_5m": wallet.get("net_in_volume_5m"),
            "net_in_volume_1m": wallet.get("net_in_volume_1m"),
            "fdv": wallet.get("fdv"),
            "market_cap": wallet.get("market_cap"),
        }
        extracted_data.append(data)
    return extracted_data




def get_addresses_and_memecoin_info():
    list_of_memecoins = []  # To store memecoin information
    addresses = []  # To store token addresses

    # Fetch data from the API
    response = requests.get(
        "https://api.dexscreener.com/token-profiles/latest/v1",
        headers={}
    )
    
    # Parse the JSON response
    dex_screen_lst = response.json()

    # Extract addresses
    for token in dex_screen_lst:
        addresses.append(token['tokenAddress'])

    # Fetch memecoin info for each address
    gmgn_instance = gmgn()
    for address in addresses:
        try:
            getTokenInfo = gmgn_instance.getTokenInfo(address)  # Assuming `gmgn` is previously defined
            list_of_memecoins.append(getTokenInfo)
        except Exception as e:
            # Handle errors gracefully
            print(f"Error processing address {address}: {e}")
            continue
    
    wallet_data=pd.DataFrame(fetch_wallet_data(list_of_memecoins)).dropna()

    return wallet_data

def anomaly_detection(wallet_data):
    wallet_data["anomaly_score"] = anomaly_model.predict(wallet_data.iloc[:,1:])
    bad_coins= wallet_data[wallet_data["anomaly_score"] == -1]['symbol'].tolist()
    result = "Coin anomaly list " + ", ".join(f"${coin}" for coin in bad_coins)

    return result

def get_memecoin_anomalies_and_scams():
    """
    Analyzes top memecoins for anomalies that could be indicative of scams or high-risk investments.
    This function fetches data from DEX screener and leverages Gemini capabilities (potentially GMGN API) to gather information about trending memecoins. It then employs anomaly detection techniques to identify coins with characteristics that deviate significantly from the norm.
    **Important Note:** While anomalies can suggest potential scams, they are not definitive proof. Always conduct thorough due diligence before investing in any memecoin.


    Args:
        None

    Returns:
        str: A message listing the memecoins with ticker symbol detected anomalies and  scams. Gemini should answer the question in first person grammar
    """
    wallet_data = get_addresses_and_memecoin_info()
    anomalies = anomaly_detection(wallet_data)
    return anomalies



################### FUNCTIONC CALLING FUNCTIONS  ENDS #################




# Configure Google Generative AI
genai.configure(api_key=os.environ['API_KEY']) ##insert your API key by setting set MY_API_KEY=your_actual_api_key in the terminal

llm_model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=[predict_wallet_pnl,get_memecoin_anomalies_and_scams])


# Define the input schema
class PredictionInput(BaseModel):
    nft_pl_ratio: float #nft pnl ratio is calculated by dividing nft_pnl by total pnl (realized_pnl + unrealized_pnl)
    trading_pnl_ratio: float #trading_pnl ratio is calculated by dividing trading_pnl by total pnl (realized_pnl + unrealized_pnl)
    liquidity_ratio: float #liquidity ratio is calculated by dividing number_of_active_trades by total_number_of_trades
    trading_frequency: float #trading frequency is calculated by dividing number_of_active_trades by total_number_of_trades
    nft_sales_rate: float #nft sales rate is calculated by dividing number_of_nft_sales by total_number_of_nft_trades


class PromptInput(BaseModel):
    prompt: str


app = FastAPI(
    title="Trading PnL Prediction API",
    description="Predicts trading profit and loss using a Random Forest model and coin scam anomaly detection",
    version="2.0.0"
)





@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome to the Trading PnL Prediction API"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@app.post("/rf/predict")
async def predict(input_data: PredictionInput):
    # Convert input to the format expected by the model
    try:
        features = np.array([[
            input_data.nft_pl_ratio,
            input_data.trading_pnl_ratio,
            input_data.liquidity_ratio,
            input_data.trading_frequency,
            input_data.nft_sales_rate
        ]])
        prediction = model.predict(features)
        return {"prediction": prediction[0]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

    
@app.post("/llm/predict")
async def llm_predict(prompt_input: PromptInput):
    """
    Use the LLM to process the user-provided prompt and call `predict_wallet_pnl`.
    """
    chat = llm_model.start_chat(enable_automatic_function_calling=True) #ensure enable_automatic_function_calling=True. Starts the Chat

    # Send the user-provided prompt to the LLM
    try:
        result = chat.send_message(prompt_input.prompt).text #outputs the text
        return {"llm_response": result} #returns as a result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


