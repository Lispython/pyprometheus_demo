current_dir = $(shell pwd)


default: clean-pyc docker-start

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

docker-clean: docker-clean-containers

docker-clean-containers:
	docker ps -q -f status=exited | xargs docker rm

docker-build:
	@echo "Run development services via docker"
	sudo docker-compose  -f compose-uwsgi.yml build --force-rm #--no-cache

docker-stop:
	@echo "Stop docker services"
	sudo docker-compose -f compose-uwsgi.yml -f stop

docker-start:
	@echo "Run development services via docker"
	docker-compose -f compose-uwsgi.yml up --force-recreate

tank:
	@echo "Tank load"
	docker run --rm --net pyprometheusdemo_default --link dev_pyprometheus_flask_app:dev_flask_app -v $(current_dir)/loadtest/:/var/loadtest/ direvius/yandex-tank
