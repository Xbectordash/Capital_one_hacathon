# 🌾 FarmMate Agricultural AI - Windows-Compatible Commands
# Note: For Windows users, use the PowerShell scripts instead!

.PHONY: help start stop logs

help: ## Show available commands
	@echo "🌾 FarmMate Agricultural AI"
	@echo "============================="
	@echo ""
	@echo "💡 WINDOWS USERS: Use these instead:"
	@echo "   .\\scripts\\start-farmmate.ps1    # Start all services"
	@echo "   docker-compose logs -f          # View logs"
	@echo "   docker-compose down             # Stop services"
	@echo ""
	@echo "🐧 LINUX/MAC USERS:"
	@echo "   make start                      # Start all services"
	@echo "   make logs                       # View logs"  
	@echo "   make stop                       # Stop services"

start: ## Start all services (Linux/Mac)
	@echo "🚀 Starting FarmMate services..."
	docker-compose up --build -d

stop: ## Stop all services
	@echo "🛑 Stopping FarmMate services..."
	docker-compose down

logs: ## View service logs
	docker-compose logs -f

health: ## Check service health (requires curl)
	@curl -f http://localhost:8000/health && echo " ✅ AI Server OK"
	@curl -f http://localhost:5000/health && echo " ✅ Express OK"
	@curl -f http://localhost:3000 && echo " ✅ Frontend OK"
