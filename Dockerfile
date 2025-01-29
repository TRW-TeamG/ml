FROM python:3.11-slim

WORKDIR /code

# Install git for cloning the repository
RUN apt-get update && apt-get install -y git

# Copy requirements first for better caching
COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Clone and install gmgn-wrapper
RUN git clone https://github.com/myx0m0p/gmgnai-wrapper.git && \
    cd gmgnai-wrapper && \
    echo "from setuptools import setup\nsetup(name='gmgn',packages=['gmgn'])" > setup.py && \
    pip install .

# Copy the rest of the application
COPY ./app /code/app
COPY model.pkl /code/
COPY anomaly_model.pkl /code/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
