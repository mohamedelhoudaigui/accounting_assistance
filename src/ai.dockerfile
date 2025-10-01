FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
	tesseract-ocr \
	curl \
    ca-certificates \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

WORKDIR /app

RUN node --version && npm --version

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

RUN mkdir upload

COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5555"]
