FROM python:3.12

ENV PYTHONPATH=/data

WORKDIR /data/api

COPY requirements.txt .

RUN apt-get update && apt-get install -y && pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]