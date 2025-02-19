FROM python:3.11-slim
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

WORKDIR /app
ENV PYTHONPATH=/app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 9090

