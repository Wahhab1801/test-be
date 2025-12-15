FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
ENV PIP_PROGRESS_BAR=off PIP_DISABLE_PIP_VERSION_CHECK=1
RUN pip install --no-cache-dir --quiet -r requirements.txt

# Copy application code
COPY agent.py .
COPY dispatch.py .

# Run the agent
CMD ["python", "agent.py", "start"]
