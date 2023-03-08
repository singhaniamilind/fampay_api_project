FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]