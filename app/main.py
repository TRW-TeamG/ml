import uvicorn
from fastapi import FastAPI
from typing import Dict
import uvicorn
import pickle
import numpy as np 
from pydantic import BaseModel
import google.generativeai as genai
import os
pickle_in=open("app/model.pkl", "rb") 
model = pickle.load(pickle_in)


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



# Configure Google Generative AI
genai.configure(api_key=os.environ['MY_API_KEY']) ##insert your API key by setting set MY_API_KEY=your_actual_api_key in the terminal

llm_model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=[predict_wallet_pnl])


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
    description="Predicts trading profit and loss using a Random Forest model",
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


