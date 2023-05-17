
setup:
	docker-compose up -d
down:
	docker-compose down
testing:
	docker-compose exec -T airflow-worker bash -c "pip3 install pytest"
	docker-compose exec -T airflow-worker bash -c "pytest"
