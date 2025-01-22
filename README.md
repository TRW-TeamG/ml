
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

### **3. Build and Run with Docker**
1. **Build the Docker Image**
   ```bash
   docker build -t my-ml-api .
   ```

2. **Run the Docker Container**
   ```bash
   docker run -p 8000:8000 my-ml-api
   ```

### **4. Access the API**
- The API will be available at: `http://localhost:8000`
- Documentation (Swagger UI): `http://localhost:8000/docs`

---

## **Usage**

### **1. Example Input**
Save the following JSON in a file (e.g., `input.json`):
```json
{
  "feature_1": 5.1,
  "feature_2": 3.5,
  "feature_3": 1.4,
  "feature_4": 0.2
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
  "prediction": "class_label"
}
```

---

## **Development Notes**
- Ensure that `model.pkl` is updated whenever the model is retrained.
- To modify API logic, update `main.py`.

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
