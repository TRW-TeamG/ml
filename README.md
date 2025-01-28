# ML Model Deployment with FastAPI and Docker

This repository contains a Random Forest Machine Learning model as well as an Isolation Forest Anomaly Detection Model integrated with Google Gemini's API. This is served through a FastAPI application. The application is containerized with Docker, making it easy to deploy and use across environments. 🎉

---

## **Project Structure**

```
.
├── app/                         # Create .env
│   ├── main.py                  # FastAPI application code
│   ├── .env                     # Recommended to have a virtual environment to store your keys
├── .dockerignore                 # Added docker files and API
├── .gitignore                    # Create .gitignore
├── Dockerfile                    # Added docker files and API
├── README.md                     # Update README.md
├── anomaly_model.pkl             # Updated LLM to include anomaly detection
├── model.pkl                     # Create model.pkl
├── requirements.txt              # Adjusted coder

```

---

## **Features**
- 🚀 **FastAPI Backend**: Serves the ML model as a REST API.
- 📦 **Dockerized**: Fully containerized for portability.
- 📄 **Example Input**: JSON file to test API endpoints.
- 🛠️ **Customizable**: Easily extend or modify the ML model and logic.
- 🔑 **Google Gemini API Integration**: Requires a free Google Gemini API key.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-name>
```

### **2. Install Dependencies**
If running locally without Docker:
```bash
pip install -r requirements.txt
```

You'll need to manually install gmgn-wrapper from 1f1n by cloning the repo (https://github.com/myx0m0p/gmgnai-wrapper/tree/main) 

Next, create a setup.py for this package since it doesnt have one. 

change directory to the cloned repo  

``` 
cd path\to\gmgn-wrapper
```  
After that, enter the following command in your terminal

``` 
pip install .
```  

After that, you can navigate back to your repository and ```import gmgn``` as a regular package. 


### **3. Add API Key**
You need a free Google Gemini API key to use the application. (https://ai.google.dev/gemini-api/docs/api-key?authuser=1)  Add your API key to a `.env` file in the root directory:
```plaintext
API_KEY=your-google-api-key
```

### **4. Build and Run with Docker**
1. **Build the Docker Image**
   ```bash
   docker build -t my-ml-api .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -p 8000:8000 my-ml-api
   ```

### **5. Access the API**
- The API will be available at: `http://localhost:8000`
- Documentation (Swagger UI): `http://localhost:8000/docs`

---

## **Usage**

### **1. Example Input**
Save the following JSON in a file (e.g., `input.json`):
```json
{
  "nft_pl_ratio": 0.8,
  "trading_pnl_ratio": 0.7,
  "liquidity_ratio": 0.6,
  "trading_frequency": 1.2,
  "nft_sales_rate": -0.3
}
```

### **2. Make a Prediction**
Using `curl`:
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d @input.json
```

#### Response:
```json
{
  "prediction": 0.435
}
```

### Using the LLM to predict PnL:
```curl -X POST "http://127.0.0.1:8000/llm/predict" \
-H "Content-Type: application/json" \
-d '{
  "prompt": "Calculate the PNL of a wallet with an NFT PNL ratio of 0.5, trading PNL ratio of 0.3, liquidity ratio of 0.7, trading frequency of 0.2, and NFT sales rate of 0.4. Also, detect any anomalies in the top memecoins."
}'
```

#### Response:
```json
{
  "prediction": "The predicted PNL of the wallet is 2.2.  Note that this is just a prediction based on the provided data and the model used by the `predict_wallet_pnl` function.  The actual PNL may vary.\n"
}
```

### Using the LLM to detect scams or anomalies among the top trending memecoins in DEXSCREENER:
```curl -X 'POST' \
  'http://127.0.0.1:8000/llm/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "Which trending memecoins might be rugpulls or scams"
}'
```

Response:
```json
{
  "llm_response": "I have analyzed top trending memecoins and detected anomalies in the following: $Wallahi im fucked, $shut up, $AI War, $Kiss, $aipump, $DADDY DOGE, $Pets, $Official Taylor Swift, $Trenches, $OFFICIAL FIFA TOKEN, $Maltipoo, $PVPAI.  These anomalies could be indicative of scams or high-risk investments.  However, it is important to remember that this is not definitive proof of a scam, and you should always conduct your own thorough due diligence before investing in any memecoin.\n"
}
```




---

## **Development Notes**
- Ensure that `model.pkl`  and ``anomaly_model.pkl` is updated whenever the model is retrained.
- To modify API logic, update `main.py`.
- Add your Google Gemini API key to the `.env` file before running the application.

---



## **Contributing**
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

Special thanks to 1f1n for providing the use of the [wrapper](https://github.com/1f1n/gmgnai-wrapper)
