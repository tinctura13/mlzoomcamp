FROM python:3.11-slim

RUN apt-get update && apt-get install -y g++ cmake libopenblas-dev zlib1g-dev && rm -rf /var/lib/apt/lists/*

RUN pip install pipenv

WORKDIR /app
COPY ["Pipfile", "Pipfile.lock", "./"]

RUN pipenv install --system --deploy

COPY ["app.py", "model.pkl", "./"]

EXPOSE 9696 

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:9696", "app:app"]