# ARIA CrewAI Research Assistant

## 🚀 Enhanced with 503 Error Prevention and Health Monitoring

ARIA is a research-oriented AI assistant system that uses CrewAI to orchestrate multiple AI agents for content generation, fact-checking, summarization, and academic research. This enhanced version includes comprehensive health monitoring, error prevention, and deployment readiness to eliminate **503 Service Temporarily Unavailable** errors.

## ✨ Key Features

### Core Functionality
- **Multi-Agent Research Pipeline**: Coordinated agents for research, fact-checking, summarization, writing, and review
- **Configurable Workflows**: YAML-based agent and task configuration
- **Tool Integration**: Extensible tool system for external API integration
- **Sequential Processing**: Step-by-step task execution with dependency management

### Enhanced Reliability (NEW)
- **🏥 Health Check System**: Comprehensive validation of system status and readiness
- **🔄 Robust Startup**: Retry logic and graceful error handling for initialization
- **📊 Resource Monitoring**: Real-time tracking of CPU, memory, and disk usage
- **🌐 API Connectivity Testing**: External API validation with timeout handling
- **⚠️ Error Handling**: Structured error tracking, categorization, and alerting
- **🐳 Production Ready**: Docker deployment with health endpoints

## 🛠️ Quick Start

### Prerequisites
- Python 3.10+
- Optional: OpenAI API key
- Optional: HuggingFace API token

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ARIA

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Set up environment variables (optional)
cp .env.example .env
# Edit .env with your API keys
```

### Health Check (Recommended First Step)

```bash
# Validate environment and configuration
python src/aria/main.py validate

# Run comprehensive health check
python src/aria/main.py health
```

### Running ARIA

#### Option 1: With Health Monitoring (Recommended)
```bash
# Run with full health monitoring and error prevention
python src/aria/main.py run
```

#### Option 2: Web Server Mode
```bash
# Start as web server with health endpoints
python src/aria/main.py server --host 0.0.0.0 --port 8000

# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/deep
```

#### Option 3: Basic Mode (Fallback)
```bash
# Run without health monitoring (if issues with enhanced features)
python src/aria/main.py run-basic
```

### Docker Deployment

```bash
# Using Docker Compose (recommended for production)
docker-compose up -d

# Check deployment health
curl http://localhost:8000/health
```

## 📊 Health Monitoring

### Health Check Endpoints

When running in server mode, ARIA provides several health endpoints:

- `GET /health` - Basic health check for load balancers
- `GET /health/deep` - Comprehensive health check with agent testing
- `GET /metrics` - System and application metrics
- `GET /status` - Simple status information

### Command Line Health Checks

```bash
# Quick health check
python src/aria/main.py health

# Environment validation
python src/aria/main.py validate

# Run test suite
python src/aria/main.py test
```

## 🚨 Troubleshooting 503 Errors

### Common Causes and Solutions

#### 1. Configuration Issues
```bash
# Diagnose configuration problems
python src/aria/main.py validate

# Check specific issues
curl http://localhost:8000/health/deep
```

#### 2. Resource Exhaustion
```bash
# Check resource usage
curl http://localhost:8000/metrics

# Monitor in real-time
watch -n 5 'curl -s http://localhost:8000/metrics | jq .system.resources'
```

#### 3. API Connectivity
```bash
# Test API connections
python src/aria/main.py health

# Check specific APIs
curl http://localhost:8000/health/deep | jq .api_connectivity
```

### Error Categories

The system categorizes errors for better diagnosis:
- **Startup**: Initialization and configuration errors
- **Configuration**: YAML and settings issues
- **Agent**: Agent creation and execution problems
- **API**: External service connectivity issues
- **Resource**: System resource constraints

## 📁 Project Structure

```
ARIA/
├── src/aria/
│   ├── main.py              # Enhanced main entry point
│   ├── crew.py              # CrewAI orchestration
│   ├── health.py            # Health check system
│   ├── robust_startup.py    # Startup with retry logic
│   ├── error_handling.py    # Error management
│   ├── monitoring.py        # Resource monitoring
│   ├── validation.py        # Environment validation
│   ├── api_testing.py       # API connectivity testing
│   ├── server.py            # Web server with health endpoints
│   ├── config/
│   │   ├── agents.yaml      # Agent definitions
│   │   └── tasks.yaml       # Task definitions
│   └── tools/               # Custom tools
├── tests/
│   └── test_health_systems.py  # Test suite
├── knowledge/
│   └── user_preference.txt  # User preferences
├── logs/                    # Application logs
├── docker-compose.yml       # Docker deployment
├── Dockerfile              # Container definition
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
└── DEPLOYMENT_GUIDE.md    # Detailed deployment guide
```

## For More Information

See the complete [Deployment Guide](DEPLOYMENT_GUIDE.md) for:
- Detailed troubleshooting steps
- Production deployment patterns
- Kubernetes configuration
- Monitoring and alerting setup
- Performance optimization tips

---

**Enhanced ARIA v0.2.0** - Now with comprehensive health monitoring and 503 error prevention! 🎉
