FROM python:3.10-alpine

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt to the container
COPY backend/src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend and agent code to the container
COPY backend backend/
COPY agent agent/
EXPOSE 8000

WORKDIR /app/backend/src

# Define the command to run the Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]