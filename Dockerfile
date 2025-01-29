FROM python:3.11-slim
# Set the working directory in the container

WORKDIR /code


# Upgrade pip and install dependencies

COPY ./requirements.txt  /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the gmgnai-wrapper folder into the container
COPY ./gmgnai-wrapper /code/gmgnai-wrapper
# Copy the app folder into the container

COPY ./app /code/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app","--host", "0.0.0.0", "--port", "8000"]
