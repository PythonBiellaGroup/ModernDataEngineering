.PHONY: docker

airflow_launch:
	docker-compose up --build -d --remove-orphans

airflow_clean:
	docker-compose down -v

ui:
	docker-compose -f "docker-compose.app.yml" up --build -d 

check:
	docker ps -a | grep "moderndataengineering"

stop:
	docker-compose down

stop_volumes:
	docker-compose down -v

volume_prune:
	docker volume prune

volume_list:
	docker volume list