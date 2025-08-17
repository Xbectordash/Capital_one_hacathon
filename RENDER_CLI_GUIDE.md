# Render CLI Deployment Guide

## Install Render CLI
```bash
# Install via npm
npm install -g @render/cli

# Or download from: https://render.com/docs/cli
```

## Login to Render
```bash
render login
```

## Deploy using render.yaml
```bash
# Navigate to your project directory
cd /path/to/Capital_one_hacathon

# Deploy all services defined in render.yaml
render deploy

# Deploy specific service
render deploy --service farmmate-ai-server
```

## Check deployment status
```bash
render services list
render services logs farmmate-ai-server
```
