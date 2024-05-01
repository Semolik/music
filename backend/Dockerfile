# Stage 1: Building Python dependencies
FROM tiangolo/uvicorn-gunicorn:python3.10-slim
WORKDIR /backend

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

COPY /backend/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Set the command to run your application
CMD uvicorn main:app --host 0.0.0.0 --port 8000

