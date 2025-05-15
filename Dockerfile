FROM python:3.10-slim

# Avoid prompts during install
ENV DEBIAN_FRONTEND=noninteractive

# Install Chrome and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set CHROME env so Selenium finds it
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${PATH}:/usr/bin/chromium"

# App setup
WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

