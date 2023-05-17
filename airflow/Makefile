
setup:
	docker compose up -d
	sleep(90)
down:
	docker compose down

testing:
	docker exec airflow-airflow-worker-1 pytest	
