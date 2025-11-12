.PHONY: start stop clean build logs

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