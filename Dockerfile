FROM python:3.10-slim

# Install system packages and Docker CLI
RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
        netcat-traditional \
        nano \
        procps \
        iproute2 \
        iputils-ping \
        ca-certificates \
        gnupg \
        lsb-release && \
    mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli containerd && \
    rm -rf /var/lib/apt/lists/*

# Optional: install nerdctl for containerd
RUN curl -sSL https://github.com/containerd/nerdctl/releases/download/v1.7.4/nerdctl-1.7.4-linux-amd64.tar.gz | tar -xz -C /usr/local/bin

# Install Python dependencies
RUN pip install flask requests

# Copy application files
COPY app.py /app.py
COPY templates /templates
COPY static /static

# Environment setup
ENV FLASK_APP=/app.py

EXPOSE 8080

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
