# Dockerfile

# pull the official docker image
FROM python:3.9.4-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# set work directory
COPY ./app /app

CMD ["python3", "./app/main.py"]