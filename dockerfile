FROM python:3.10.11-slim

# Set the working directory inside the container
WORKDIR /src

# Copy requirements first (for better caching)
COPY requirements.txt /src/

# Install Python dependencies
# --no-cache-dir prevents pip from storing downloaded package files in cache
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and its dependencies
RUN playwright install-deps
RUN playwright install chromium

# Install Xvfb and clean up in one layer to reduce image size
RUN apt-get update && apt-get install -y xvfb xauth \
    && rm -rf /var/lib/apt/lists/*

# Copy source code (this will be overridden by volume mount in development)
COPY src/ /src/

# Default command - can be overridden in docker-compose.yml
CMD ["sh", "-c", "echo 'Running script...' && xvfb-run -a python -u checkin.py"]