# ML Model Deployment with FastAPI and Docker

This repository contains a Random Forest Machine Learning model served through a FastAPI application. The application is containerized with Docker, making it easy to deploy and use across environments. 🎉

---

## **Project Structure**

```
.
├── app/
│   ├── main.py                 # FastAPI application code
│   ├── model.pkl               # Serialized ML model
│   ├── preprocess.py           # Preprocessing logic (if applicable)
│   ├── mlmodel.py              # Model training/testing script
├── Dockerfile                  # Docker build instructions
├── docker-compose.yaml         # Optional for multi-container setups
├── requirements.txt            # Python dependencies
├── exampleData.json            # Example input data for testing
├── README.md                   # Project documentation (you are here!)
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

change directory to the cloned repo  ``` cd path\to\gmgn-wrapper``` and run ```pip install . `` a

After that, you can navigate back to your repository and ```import gmgn`` as a regular package. 


### **3. Add API Key**
You need a free Google Gemini API key to use the application. `https://ai.google.dev/gemini-api/docs/api-key?authuser=1`  Add your API key to a `.env` file in the root directory:
```plaintext
GOOGLE_API_KEY=your-google-api-key
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

Response:
```json
{
  "prediction": 0.435
}
```

---

## **Development Notes**
- Ensure that `model.pkl` is updated whenever the model is retrained.
- To modify API logic, update `main.py`.
- Add your Google Gemini API key to the `.env` file before running the application.

---

## **Repository Contents**
- **`mlmodel.py`**: Python file used to make the ML model
- **`Dockerfile`**: Defines the environment for containerized deployment.
- **`docker-compose.yaml`**: Optional file for multi-container orchestration.
- **`requirements.txt`**: Lists Python dependencies.
- **`exampleData.json`**: Sample input for testing the API.

---

## **Contributing**
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

## **License**
This project is licensed under the [MIT License](LICENSE).

Special thanks to 1f1n for providing the use of the [wrapper](https://github.com/1f1n/gmgnai-wrapper)
