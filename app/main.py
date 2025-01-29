import uvicorn
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, Security
from typing import Dict
import uvicorn
import pickle
import numpy as np 
from pydantic import BaseModel
from gmgn import gmgn
import requests
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

model = pickle.load(open("model.pkl", "rb"))
anomaly_model = pickle.load(open("anomaly_model.pkl", "rb"))

security = HTTPBearer()
API_TOKEN = os.getenv("API_TOKEN", "tati-tati-tati")  # Get from environment variable

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return credentials.credentials

def predict_wallet_pnl(nft_pl_ratio:float, trading_pnl_ratio:float,
                      liquidity_ratio:float, trading_frequency:float,
                      nft_sales_rate:float):
    input_data = np.array([[nft_pl_ratio, trading_pnl_ratio,
                   liquidity_ratio, trading_frequency, nft_sales_rate]])
    prediction = model.predict(input_data)
    return float(prediction[0])

def fetch_wallet_data(wallets):
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
    list_of_memecoins = []
    addresses = []
    response = requests.get(
        "https://api.dexscreener.com/token-profiles/latest/v1",
        headers={}
    )
    dex_screen_lst = response.json()
    for token in dex_screen_lst:
        addresses.append(token['tokenAddress'])
    gmgn_instance = gmgn()
    for address in addresses:
        try:
            getTokenInfo = gmgn_instance.getTokenInfo(address)
            list_of_memecoins.append(getTokenInfo)
        except Exception as e:
            print(f"Error processing address {address}: {e}")
            continue
    wallet_data=pd.DataFrame(fetch_wallet_data(list_of_memecoins)).dropna()
    return wallet_data

def anomaly_detection(wallet_data):
    wallet_data["anomaly_score"] = anomaly_model.predict(wallet_data.iloc[:,1:])
    bad_coins= wallet_data[wallet_data["anomaly_score"] == -1]['symbol'].tolist()
    result = "" + ", ".join(f"${coin}" for coin in bad_coins)

    return result

def get_memecoin_anomalies_and_scams():
    wallet_data = get_addresses_and_memecoin_info()
    anomalies = anomaly_detection(wallet_data)
    return anomalies



class PredictionInput(BaseModel):
    nft_pl_ratio: float
    trading_pnl_ratio: float
    liquidity_ratio: float
    trading_frequency: float
    nft_sales_rate: float

class PromptInput(BaseModel):
    prompt: str

app = FastAPI(
    title="Trading PnL and Scamcoin Prediction API",
    description="Predicts trading profit and loss using a Random Forest model and memecoin scam detection via Isolation Forest",
    version="2.0.0"
)


@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "Welcome RF PnL and Scamcoin Prediction API"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@app.post("/rf/predict")
async def predict(input_data: PredictionInput, token: str = Depends(verify_token)):
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

    
@app.post("/scamcoins_isoforest/predict")
async def scamcoin_prediction():
    """
    Fetches the Open DEXScreener API and returns suspected scam coins/rugpulls via isolation forest anomaly detection
    """
    # Send the user-provided prompt to the LLM
    try:
        result = get_memecoin_anomalies_and_scams()
        return {"scam_memecoins": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
