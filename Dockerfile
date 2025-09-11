# Dockerfile for ARIA CrewAI Application
# Optimized for preventing 503 Service Temporarily Unavailable errors

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV ARIA_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app directory
WORKDIR /app

# Create logs directory
RUN mkdir -p /app/logs

# Copy dependency files first (for better caching)
COPY pyproject.toml ./
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Copy source code
COPY src/ ./src/
COPY knowledge/ ./knowledge/
COPY tests/ ./tests/

# Create non-root user for security
RUN groupadd -r aria && useradd -r -g aria aria
RUN chown -R aria:aria /app
USER aria

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python src/aria/main.py health || exit 1

# Expose port
EXPOSE 8000

# Default command - run with health monitoring
CMD ["python", "src/aria/main.py", "server", "--host", "0.0.0.0", "--port", "8000"]