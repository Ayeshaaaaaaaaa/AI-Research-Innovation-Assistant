# # Dockerfile for ARIA CrewAI Application
# # Optimized for stability and Docker Hub deployment

# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONPATH=/app \
#     ARIA_ENV=production

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Create app directory
# WORKDIR /app

# # Create logs directory
# RUN mkdir -p /app/logs

# # Copy dependency files first (for better caching)
# COPY pyproject.toml ./ 
# COPY requirements.txt* ./ 

# # Install Python dependencies

# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir hatchling && \
#     if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# # Copy source code
# COPY src/ ./src/
# COPY knowledge/ ./knowledge/
# COPY tests/ ./tests/

# # Create non-root user for security
# RUN groupadd -r aria && useradd -r -g aria aria
# RUN chown -R aria:aria /app
# USER aria

# # Expose port
# EXPOSE 8000

# # Default command - run the app
# CMD ["python", "src/aria/main.py", "server", "--host", "0.0.0.0", "--port", "8000"]
# Dockerfile for ARIA CrewAI Application
# Optimized for stability and Docker Hub deployment

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    ARIA_ENV=production

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
    pip install --no-cache-dir hatchling && \
    pip install --no-cache-dir hatchling fastapi uvicorn && \
    if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src \
    ARIA_ENV=production
# Copy source code
COPY src/ ./src/
COPY knowledge/ ./knowledge/
COPY tests/ ./tests/

# Create non-root user for security
RUN groupadd -r aria && useradd -r -g aria aria

# Fix: Create home directory + .local/share for CrewAI storage
RUN mkdir -p /home/aria/.local/share && \
    chown -R aria:aria /home/aria && \
    chown -R aria:aria /app

USER aria

# Expose port
EXPOSE 8000

# Default command - run the app
# CMD ["python", "src/aria/main.py", "server", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "src.aria.main:app", "--host", "0.0.0.0", "--port", "8000"]


# FROM python:3.11-slim

# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONPATH=/app \
#     ARIA_ENV=production

# # Install system dependencies
# RUN apt-get update && apt-get install -y \
#     gcc \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Create app directory
# WORKDIR /app

# # Create logs directory
# RUN mkdir -p /app/logs

# # Copy dependency files first (for better caching)
# COPY pyproject.toml ./ 
# COPY requirements.txt* ./ 

# # Install Python dependencies
# RUN pip install --no-cache-dir --upgrade pip && \
#     pip install --no-cache-dir hatchling && \
#     pip install --no-cache-dir hatchling fastapi uvicorn && \
#     if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
# # Set environment variables
# ENV PYTHONUNBUFFERED=1 \
#     PYTHONPATH=/app/src \
#     ARIA_ENV=production
# # Copy source code
# COPY src/ ./src/
# COPY knowledge/ ./knowledge/
# COPY tests/ ./tests/

# # Create non-root user for security
# RUN groupadd -r aria && useradd -r -g aria aria

# # Fix: Create home directory + .local/share for CrewAI storage
# RUN mkdir -p /home/aria/.local/share && \
#     chown -R aria:aria /home/aria && \
#     chown -R aria:aria /app

# USER aria

# # Expose port
# EXPOSE 8000

# # Default command - run the app
# # CMD ["python", "src/aria/main.py", "server", "--host", "0.0.0.0", "--port", "8000"]
# CMD ["uvicorn", "src.aria.main:app", "--host", "0.0.0.0", "--port", "8000"]
