# ARIA CrewAI Deployment Guide

## 503 Error Resolution Implementation

This guide covers the deployment of ARIA CrewAI with comprehensive health monitoring and error prevention to resolve **503 Service Temporarily Unavailable** errors.

## Overview

The enhanced ARIA system includes:

- **Health Check System**: Comprehensive validation of system status
- **Robust Startup**: Retry logic and graceful error handling
- **Resource Monitoring**: Real-time system resource tracking
- **API Connectivity Testing**: External API validation and timeout handling
- **Error Handling**: Structured error tracking and alerting
- **Deployment Configuration**: Production-ready Docker setup

## Quick Start

### 1. Basic Health Check

```bash
# Test system health
python src/aria/main.py health

# Validate environment and configuration
python src/aria/main.py validate
```

### 2. Run with Health Monitoring

```bash
# Run with full health monitoring (recommended)
python src/aria/main.py run

# Run in basic mode (fallback)
python src/aria/main.py run-basic
```

### 3. Web Server Mode

```bash
# Start web server with health endpoints
python src/aria/main.py server --host 0.0.0.0 --port 8000
```

## Deployment Options

### Option 1: Docker Deployment (Recommended)

1. **Build and run with Docker Compose:**

```bash
# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Build and start services
docker-compose up -d

# Check health
curl http://localhost:8000/health
```

2. **Check deployment status:**

```bash
# View logs
docker-compose logs -f aria

# Check health endpoints
curl http://localhost:8000/health/deep
curl http://localhost:8000/metrics
```

### Option 2: Manual Deployment

1. **Install dependencies:**

```bash
pip install -r requirements.txt
pip install -e .
```

2. **Set environment variables:**

```bash
export OPENAI_API_KEY="your-openai-key"
export HF_TOKEN="your-huggingface-token"
export LOG_LEVEL="INFO"
```

3. **Run pre-deployment checks:**

```bash
# Validate environment
python src/aria/main.py validate

# Test API connectivity
python src/aria/main.py health
```

4. **Start the application:**

```bash
# With health monitoring
python src/aria/main.py run

# As web server
python src/aria/main.py server
```

## Health Check Endpoints

The ARIA server provides multiple health check endpoints:

### GET /health
Basic health check for load balancers:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "config_files": true,
  "environment_vars": true,
  "system_resources": {...}
}
```

### GET /health/deep
Comprehensive health check including agent initialization:

```bash
curl http://localhost:8000/health/deep
```

### GET /metrics
Application and system metrics:

```bash
curl http://localhost:8000/metrics
```

### GET /status
Simple status check:

```bash
curl http://localhost:8000/status
```

## Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `OPENAI_API_KEY` | OpenAI API key for LLM operations | Optional | - |
| `HF_TOKEN` / `HF_TKN` | HuggingFace API token | Optional | - |
| `LOG_LEVEL` | Logging level (DEBUG, INFO, WARNING, ERROR) | No | INFO |
| `MAX_CONCURRENT_TASKS` | Maximum concurrent task execution | No | 5 |
| `API_TIMEOUT` | Timeout for external API calls (seconds) | No | 30 |
| `ARIA_CONFIG_DIR` | Custom configuration directory | No | src/aria/config |

### Configuration Files

- `src/aria/config/agents.yaml` - Agent definitions
- `src/aria/config/tasks.yaml` - Task definitions
- `knowledge/user_preference.txt` - User preferences

## Monitoring and Troubleshooting

### Health Check Validation

The system performs the following validations:

1. **Python Version**: Ensures Python 3.10+ compatibility
2. **Environment Variables**: Validates API tokens and configuration
3. **Directory Structure**: Checks required files and directories
4. **System Resources**: Monitors CPU, memory, and disk usage
5. **Configuration Files**: Validates YAML syntax and structure
6. **API Connectivity**: Tests external API endpoints
7. **Agent Initialization**: Verifies agent creation process

### Common Issues and Solutions

#### 1. 503 Service Temporarily Unavailable

**Symptoms:**
- Server shows "online" but returns 503 errors
- Health check endpoints return 503

**Diagnosis:**
```bash
# Check detailed health status
curl http://localhost:8000/health/deep

# Check logs
docker-compose logs aria
```

**Common Causes and Solutions:**

1. **Configuration Issues:**
   ```bash
   # Validate configuration
   python src/aria/main.py validate
   ```

2. **Missing API Keys:**
   ```bash
   # Check environment variables
   echo $OPENAI_API_KEY
   echo $HF_TOKEN
   ```

3. **Resource Exhaustion:**
   ```bash
   # Check system resources
   curl http://localhost:8000/metrics
   ```

4. **Agent Initialization Failures:**
   ```bash
   # Test agent initialization
   python src/aria/main.py health
   ```

#### 2. High Memory Usage

**Solutions:**
- Increase container memory limits in `docker-compose.yml`
- Monitor resource usage via `/metrics` endpoint
- Implement request queuing for high load

#### 3. API Timeout Errors

**Solutions:**
- Increase `API_TIMEOUT` environment variable
- Check API connectivity: `curl http://localhost:8000/health/deep`
- Implement circuit breaker pattern (already included)

#### 4. Configuration Validation Failures

**Solutions:**
- Validate YAML syntax in config files
- Ensure all required agents and tasks are defined
- Check agent-task consistency

### Log Analysis

Application logs include:

- **Startup Events**: Initialization progress and failures
- **Health Check Results**: Detailed validation outcomes
- **API Connectivity**: External service status
- **Resource Monitoring**: System resource usage warnings
- **Error Tracking**: Categorized error reporting

Log locations:
- Docker: `docker-compose logs aria`
- Manual: `logs/aria.log`

### Performance Monitoring

Monitor these metrics for optimal performance:

1. **Response Time**: Average API response time
2. **Success Rate**: Request success percentage
3. **Resource Usage**: CPU, memory, disk utilization
4. **Error Rate**: Categorized error frequencies
5. **API Connectivity**: External service availability

## Production Deployment Checklist

### Pre-Deployment

- [ ] Environment variables configured
- [ ] Configuration files validated (`python src/aria/main.py validate`)
- [ ] API connectivity tested (`python src/aria/main.py health`)
- [ ] Resource requirements met (1GB+ RAM, 5GB+ disk)
- [ ] Network connectivity to external APIs verified

### Deployment

- [ ] Container built successfully
- [ ] Health check endpoints responding
- [ ] Monitoring systems configured
- [ ] Log aggregation set up
- [ ] Resource limits configured
- [ ] Backup and recovery procedures established

### Post-Deployment

- [ ] Health endpoints returning 200 OK
- [ ] Application logs streaming
- [ ] Resource usage within limits
- [ ] Error rates below threshold (<5%)
- [ ] API connectivity stable
- [ ] Response times acceptable (<2s average)

### Load Balancer Configuration

For production deployments behind a load balancer:

```nginx
upstream aria_backend {
    server aria:8000 max_fails=3 fail_timeout=30s;
}

server {
    listen 80;
    
    location /health {
        proxy_pass http://aria_backend;
        proxy_connect_timeout 5s;
        proxy_read_timeout 10s;
    }
    
    location / {
        proxy_pass http://aria_backend;
        proxy_connect_timeout 10s;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
    }
}
```

### Kubernetes Deployment

Example Kubernetes configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: aria-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: aria
  template:
    metadata:
      labels:
        app: aria
    spec:
      containers:
      - name: aria
        image: aria:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: aria-secrets
              key: openai-api-key
        - name: HF_TOKEN
          valueFrom:
            secretKeyRef:
              name: aria-secrets
              key: hf-token
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
          timeoutSeconds: 10
          failureThreshold: 3
        readinessProbe:
          httpGet:
            path: /health/deep
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 15
          timeoutSeconds: 10
          failureThreshold: 2
        resources:
          requests:
            memory: "512Mi"
            cpu: "0.5"
          limits:
            memory: "2Gi"
            cpu: "1.0"
```

## Rollback Strategy

If deployment issues occur:

1. **Immediate Rollback:**
   ```bash
   # Docker
   docker-compose down
   docker-compose up -d --scale aria=0
   
   # Kubernetes
   kubectl rollout undo deployment/aria-deployment
   ```

2. **Health Check Verification:**
   ```bash
   # Verify rollback success
   curl http://localhost:8000/health
   ```

3. **Log Analysis:**
   ```bash
   # Analyze failure logs
   docker-compose logs --tail=100 aria
   ```

## Support and Troubleshooting

For additional support:

1. Run comprehensive diagnostics: `python src/aria/main.py validate`
2. Check health status: `python src/aria/main.py health`
3. Review application logs for error patterns
4. Monitor resource usage and API connectivity
5. Verify configuration file syntax and completeness

The enhanced ARIA system provides comprehensive monitoring and error handling to prevent 503 errors and ensure reliable deployment.