FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl wget netcat-traditional nano procps iproute2 iputils-ping ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install flask requests

ENV FLASK_APP=metadata_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

EXPOSE 5000

CMD ["flask", "run"]
