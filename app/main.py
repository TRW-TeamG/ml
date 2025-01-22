import uvicorn
from fastapi import FastAPI
from typing import Dict
import uvicorn
import pickle
import numpy as np 
from pydantic import BaseModel
pickle_in=open("app/model.pkl", "rb") 
model = pickle.load(pickle_in)

# Define the input schema
class PredictionInput(BaseModel):
    nft_pl_ratio: float #nft pnl ratio is calculated by dividing nft_pnl by total pnl (realized_pnl + unrealized_pnl)
    trading_pnl_ratio: float #trading_pnl ratio is calculated by dividing trading_pnl by total pnl (realized_pnl + unrealized_pnl)
    liquidity_ratio: float #liquidity ratio is calculated by dividing number_of_active_trades by total_number_of_trades
    trading_frequency: float #trading frequency is calculated by dividing number_of_active_trades by total_number_of_trades
    nft_sales_rate: float #nft sales rate is calculated by dividing number_of_nft_sales by total_number_of_nft_trades

app = FastAPI(
    title="Trading PnL Prediction API",
    description="Predicts trading profit and loss using a Random Forest model",
    version="1.0.0"
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


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


