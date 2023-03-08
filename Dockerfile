# FROM python:3.10 as builder
# WORKDIR /usr/src/app
# ENV PATH="venv/$bin=$PATH"
# RUN python3 -m venv /venv
# COPY requirements.txt ./
# RUN pip install -r requirements.txt

# FROM python:3.10-slim
# WORKDIR /usr/src/app
# ENV PATH="venv/$bin=$PATH"
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED=1

# COPY --from=builder /venv /venv
# COPY . .
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
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