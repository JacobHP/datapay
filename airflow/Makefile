
setup:
	docker-compose up -d
down:
	docker-compose down
testing:
	sudo chmod -R 777 ./logs
	docker-compose exec -T airflow-worker bash -c "pip3 install pytest"
	docker-compose exec -T airflow-worker bash -c "pytest"
