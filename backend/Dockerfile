ARG CACHEBUST=1 
FROM tiangolo/uvicorn-gunicorn:python3.10
COPY .env /app
# COPY .env.local /app/
WORKDIR /app
# install any necessary dependencies
COPY backend/requirements.txt /requirements.txt
# RUN apt-get update && apt-get install -y ffmpeg 
RUN pip install -r /requirements.txt
# copy our app code to the /app directory
COPY ./backend /app/backend
COPY ./.env /app
COPY ./.env.local /app 



# set the working directory in the container
WORKDIR /app

# when the container is run, start the API and the uvicorn server
ENTRYPOINT ["uvicorn", "backend.main:app", "--host", "0.0.0.0"]