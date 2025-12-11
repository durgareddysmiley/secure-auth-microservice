# ================================
# Stage 1: Builder
# ================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy dependency file
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ================================
# Stage 2: Runtime
# ================================
FROM python:3.11-slim AS runtime

ENV TZ=UTC

WORKDIR /app

# Install cron + timezone data
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        cron \
        tzdata \
    && ln -sf /usr/share/zoneinfo/UTC /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy ALL application files
COPY . .

# Ensure directories exist
RUN mkdir -p /data /cron && chmod 755 /data /cron


# ================================
# Copy Cron job + Scripts
# ================================

# Copy cron file into Linux cron system
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Copy cron script directory
COPY scripts/ ./scripts

# Correct permissions
RUN chmod 0644 /etc/cron.d/2fa-cron

# Register cron job
RUN crontab /etc/cron.d/2fa-cron


# ================================
# Expose FastAPI port
# ================================
EXPOSE 8080


# ================================
# Start cron + FastAPI server
# ================================
CMD service cron start && uvicorn main:app --host 0.0.0.0 --port 8080
