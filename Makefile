PACKAGE = docker-lambda-python
IMAGE_TAG = python3.6
BUILD = 1
VERSION = $(IMAGE_TAG)-build$(BUILD)

REPOSITORY = caltechads/$(PACKAGE)

#======================================================================

clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm 
	find . -name "*.pyc" -exec rm '{}' ';'

version:
	@echo ${VERSION}

force-build:
	docker build --no-cache -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:${IMAGE_TAG}
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:${VERSION}
	docker image prune -f

build:
	docker build -t ${PACKAGE}:${VERSION} .
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:${IMAGE_TAG}
	docker tag ${PACKAGE}:${VERSION} ${PACKAGE}:${VERSION}
	docker image prune -f

tag:
	docker tag ${PACKAGE}:${IMAGE_TAG} ${REPOSITORY}:${IMAGE_TAG}
	docker tag ${PACKAGE}:${VERSION} ${REPOSITORY}:${VERSION}

push: tag
	docker push ${REPOSITORY}

run:
	docker run -ti --entrypoint bash ${PACKAGE}:${IMAGE_TAG}

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
