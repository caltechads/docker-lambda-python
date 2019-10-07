VERSION = 0.2.0

#======================================================================

clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm 
	find . -name "*.pyc" -exec rm '{}' ';'

version:
	@echo ${VERSION}

force-build:
	docker build --no-cache lambda:python3.6 .
	docker tag lambda:python3.6 caltechads/lambda:python3.6
	# Delete dangling container images to help prevent disk bloat.
	docker image prune -f
	rm -rf common

build:
	docker build -f Dockerfile -t lambda:python3.6 .
	docker tag lambda:python3.6 caltechads/lambda:python3.6
	# Delete dangling container images to help prevent disk bloat.
	docker image prune -f
	rm -rf common

dev:
	docker-compose up

dev-detached:
	docker-compose up -d

docker-clean:
	docker stop $(shell docker ps -a -q)
	docker rm $(shell docker ps -a -q)

docker-destroy: docker-clean docker-destroy-db
	docker rmi -f $(shell docker images -q | uniq)
	docker image prune -f; docker volume prune -f; docker container prune -f
