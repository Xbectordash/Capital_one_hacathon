#!/bin/bash

# Enhanced Docker Startup Script for FarmMate with Monitoring
# This script manages the complete Docker-based deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.enhanced.yml"
DEV_COMPOSE_FILE="docker-compose.dev.yml"
PROJECT_NAME="farmmate"

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                    🐳 FARMMATE DOCKER DEPLOYMENT 🐳                          ║
║                     Enhanced with Comprehensive Monitoring                   ║
║                                                                              ║
║  📊 Monitoring Dashboard (Port 9000)                                        ║
║  🐍 Python AI Server (Port 8000)                                            ║
║  🚀 Express Backend (Port 5000)                                             ║
║  ⚛️  React Frontend (Port 3000)                                              ║
║  🌐 Nginx Load Balancer (Port 80)                                           ║
║  📈 Prometheus (Port 9090)                                                  ║
║  📊 Grafana (Port 3001)                                                     ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
    
    if ! docker-compose --version >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker Compose is not available. Please install docker-compose.${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker and Docker Compose are available${NC}"
}

# Function to check if ports are available
check_ports() {
    local ports=(9000 8000 5000 3000 80 9090 3001)
    local unavailable_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            unavailable_ports+=($port)
        fi
    done
    
    if [ ${#unavailable_ports[@]} -gt 0 ]; then
        echo -e "${RED}❌ The following ports are already in use: ${unavailable_ports[*]}${NC}"
        echo -e "${YELLOW}   Please stop the services using these ports or use different ports${NC}"
        return 1
    else
        echo -e "${GREEN}✅ All required ports are available${NC}"
        return 0
    fi
}

# Function to build and start services
start_services() {
    local mode=$1
    local compose_files="-f $COMPOSE_FILE"
    
    if [ "$mode" = "dev" ]; then
        compose_files="$compose_files -f $DEV_COMPOSE_FILE"
        echo -e "${YELLOW}🔧 Starting in development mode with file watching${NC}"
    else
        echo -e "${BLUE}🚀 Starting in production mode${NC}"
    fi
    
    echo -e "${PURPLE}📦 Building Docker images...${NC}"
    docker-compose $compose_files -p $PROJECT_NAME build --parallel
    
    echo -e "${PURPLE}🚀 Starting services...${NC}"
    docker-compose $compose_files -p $PROJECT_NAME up -d
    
    # Wait for services to start
    echo -e "${YELLOW}⏳ Waiting for services to start...${NC}"
    sleep 10
    
    # Check service health
    check_service_health
}

# Function to check service health
check_service_health() {
    local services=(
        "monitoring:9000:/health"
        "agent-python:8000:/health"
        "backend:5000:/api/health"
        "frontend-web:3000:/health"
    )
    
    echo -e "${BLUE}🔍 Checking service health...${NC}"
    
    for service_info in "${services[@]}"; do
        IFS=':' read -r service port path <<< "$service_info"
        local url="http://localhost:$port$path"
        local max_attempts=30
        local attempt=1
        
        while [ $attempt -le $max_attempts ]; do
            if curl -s -f "$url" >/dev/null 2>&1; then
                echo -e "${GREEN}✅ $service is healthy${NC}"
                break
            elif [ $attempt -eq $max_attempts ]; then
                echo -e "${RED}❌ $service failed to start (timeout after $max_attempts attempts)${NC}"
                echo -e "${YELLOW}   Check logs: docker-compose -p $PROJECT_NAME logs $service${NC}"
            else
                echo -e "${YELLOW}⏳ Waiting for $service... (attempt $attempt/$max_attempts)${NC}"
                sleep 2
                ((attempt++))
            fi
        done
    done
}

# Function to stop services
stop_services() {
    echo -e "${YELLOW}🛑 Stopping FarmMate services...${NC}"
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down
    echo -e "${GREEN}✅ All services stopped${NC}"
}

# Function to clean up
cleanup() {
    echo -e "${YELLOW}🧹 Cleaning up Docker resources...${NC}"
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME down -v --remove-orphans
    docker system prune -f
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

# Function to show logs
show_logs() {
    local service=$1
    if [ -z "$service" ]; then
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f
    else
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME logs -f "$service"
    fi
}

# Function to show status
show_status() {
    echo -e "${BLUE}📊 FarmMate Service Status:${NC}"
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME ps
    
    echo -e "\n${BLUE}🔗 Service URLs:${NC}"
    echo -e "${GREEN}📊 Monitoring Dashboard: http://localhost:9000${NC}"
    echo -e "${GREEN}🌾 FarmMate Web App:     http://localhost:3000${NC}"
    echo -e "${GREEN}🚀 Express Backend:      http://localhost:5000${NC}"
    echo -e "${GREEN}🐍 Python AI Server:     http://localhost:8000${NC}"
    echo -e "${GREEN}🌐 Nginx Load Balancer:  http://localhost:80${NC}"
    echo -e "${GREEN}📈 Prometheus:           http://localhost:9090${NC}"
    echo -e "${GREEN}📊 Grafana:              http://localhost:3001${NC}"
    
    echo -e "\n${BLUE}💾 Docker Resources:${NC}"
    echo "Images:"
    docker images | grep farmmate
    echo -e "\nVolumes:"
    docker volume ls | grep farmmate
}

# Function to backup data
backup_data() {
    local backup_dir="./backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$backup_dir"
    
    echo -e "${BLUE}💾 Creating backup at $backup_dir...${NC}"
    
    # Backup monitoring database
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME exec -T monitoring sqlite3 /app/data/monitoring.db .dump > "$backup_dir/monitoring.sql"
    
    # Backup Docker volumes
    docker run --rm -v "${PROJECT_NAME}_monitoring-data:/data" -v "$(pwd)/$backup_dir:/backup" alpine tar czf /backup/monitoring-data.tar.gz -C /data .
    docker run --rm -v "${PROJECT_NAME}_logs-data:/data" -v "$(pwd)/$backup_dir:/backup" alpine tar czf /backup/logs-data.tar.gz -C /data .
    
    echo -e "${GREEN}✅ Backup completed at $backup_dir${NC}"
}

# Function to restore data
restore_data() {
    local backup_dir=$1
    if [ ! -d "$backup_dir" ]; then
        echo -e "${RED}❌ Backup directory $backup_dir not found${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}🔄 Restoring from $backup_dir...${NC}"
    
    # Stop services
    stop_services
    
    # Restore volumes
    docker run --rm -v "${PROJECT_NAME}_monitoring-data:/data" -v "$(pwd)/$backup_dir:/backup" alpine tar xzf /backup/monitoring-data.tar.gz -C /data
    docker run --rm -v "${PROJECT_NAME}_logs-data:/data" -v "$(pwd)/$backup_dir:/backup" alpine tar xzf /backup/logs-data.tar.gz -C /data
    
    echo -e "${GREEN}✅ Restore completed${NC}"
}

# Function to update services
update_services() {
    echo -e "${BLUE}🔄 Updating FarmMate services...${NC}"
    
    # Pull latest images
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME pull
    
    # Rebuild and restart
    docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME up -d --build
    
    echo -e "${GREEN}✅ Services updated${NC}"
}

# Main script logic
case "${1:-start}" in
    start|up)
        check_docker
        if [ "${2}" != "--skip-port-check" ]; then
            check_ports || exit 1
        fi
        start_services "${2}"
        show_status
        
        echo -e "\n${GREEN}"
        cat << "EOF"
╔══════════════════════════════════════════════════════════════════════════════╗
║                        🎉 FARMMATE DEPLOYMENT COMPLETE! 🎉                  ║
║                          All Services Running in Docker                      ║
║                                                                              ║
║  📊 Monitoring: http://localhost:9000                                       ║
║  🌾 Web App:    http://localhost:3000                                       ║
║  🌐 Main Site:  http://localhost:80                                         ║
║                                                                              ║
║  Use './scripts/docker-farmmate.sh logs' to view logs                       ║
║  Use './scripts/docker-farmmate.sh stop' to stop all services              ║
╚══════════════════════════════════════════════════════════════════════════════╝
EOF
        echo -e "${NC}"
        ;;
        
    dev)
        check_docker
        check_ports || exit 1
        start_services "dev"
        show_status
        ;;
        
    stop|down)
        stop_services
        ;;
        
    restart)
        stop_services
        sleep 2
        check_docker
        start_services
        ;;
        
    status|ps)
        show_status
        ;;
        
    logs)
        show_logs "${2}"
        ;;
        
    cleanup|clean)
        cleanup
        ;;
        
    backup)
        backup_data
        ;;
        
    restore)
        restore_data "${2}"
        ;;
        
    update)
        update_services
        ;;
        
    build)
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME build --parallel
        ;;
        
    shell)
        service="${2:-monitoring}"
        docker-compose -f $COMPOSE_FILE -p $PROJECT_NAME exec "$service" /bin/bash
        ;;
        
    *)
        echo -e "${BLUE}🐳 FarmMate Docker Management Script${NC}"
        echo ""
        echo -e "${YELLOW}Usage: $0 {start|dev|stop|restart|status|logs|cleanup|backup|restore|update|build|shell}${NC}"
        echo ""
        echo "Commands:"
        echo "  start [--skip-port-check]  Start all services in production mode"
        echo "  dev                        Start all services in development mode"
        echo "  stop                       Stop all services"
        echo "  restart                    Restart all services"
        echo "  status                     Show service status and URLs"
        echo "  logs [service]             Show logs for all services or specific service"
        echo "  cleanup                    Stop services and clean up Docker resources"
        echo "  backup                     Create backup of data volumes"
        echo "  restore <backup_dir>       Restore from backup directory"
        echo "  update                     Update all services to latest version"
        echo "  build                      Build all Docker images"
        echo "  shell [service]            Open shell in service container (default: monitoring)"
        echo ""
        echo "Examples:"
        echo "  $0 start                   # Start all services"
        echo "  $0 dev                     # Start in development mode"
        echo "  $0 logs monitoring         # Show monitoring service logs"
        echo "  $0 shell agent-python      # Open shell in Python AI server"
        ;;
esac
