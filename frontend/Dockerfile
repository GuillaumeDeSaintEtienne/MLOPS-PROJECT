FROM python:3.9-slim

EXPOSE 8080

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY frontend/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY frontend/ .

ENTRYPOINT ["streamlit", "run", "Home.py", \
    "--server.port=8080", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.enableCORS=false", \
    "--server.enableXsrfProtection=false", \
    "--browser.gatherUsageStats=false"]