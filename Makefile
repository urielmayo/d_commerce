stop:
	docker-compose down

run:
	docker-compose up

migrations:
	docker-compose run --rm --service-ports web python manage.py makemigrations

shell:
	docker-compose run --rm --service-ports web python manage.py shell