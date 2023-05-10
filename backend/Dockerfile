ARG CACHEBUST=1 
FROM tiangolo/uvicorn-gunicorn:python3.10

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg 

# Copy .env file
COPY .env /app

# Set the working directory to /app
WORKDIR /app

# Install necessary dependencies
COPY backend/requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Copy the app code to the /app directory
COPY ./backend /app/backend
COPY ./.env /app
# Set the working directory in the container
WORKDIR /app

# When the container is run, start the API and the uvicorn server
ENTRYPOINT ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]
