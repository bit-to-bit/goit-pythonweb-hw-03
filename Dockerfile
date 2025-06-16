FROM python:3.10.18-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

COPY main.py .

COPY config.ini .

EXPOSE 3000

ENTRYPOINT ["python", "main.py"]