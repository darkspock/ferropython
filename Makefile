.PHONY: start stop clean build logs run

start:
	docker-compose up -d

stop:
	docker-compose down

clean:
	docker-compose down -v
	docker system prune -f

build:
	docker-compose build

logs:
	docker-compose logs -f

restart: stop start

run:
	uv sync
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8001

run-daemon:
	uv sync
	nohup uv run uvicorn main:app --host 0.0.0.0 --port 8001 > server.log 2>&1 &

stop-daemon:
	pkill -f "uvicorn main:app" || true