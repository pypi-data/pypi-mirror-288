# DOCKER_SERVICE_NAME
# DOCKER_HOST
# DOCKER_SERVICE_PORT
# DOCKER_RUN_OPTS

DOCKER_REPOSITORY ?= sucicada

service_name ?= $(DOCKER_SERVICE_NAME)
REMOTE_DOCKER_HOST ?= $(DOCKER_HOST)

docker_image_name := $(DOCKER_REPOSITORY)/$(service_name):latest

remote_docker := unset DOCKER_HOST; docker
ifeq ($(REMOTE),true)
	remote_docker := DOCKER_HOST=$(REMOTE_DOCKER_HOST) docker
endif

docker-build:
	$(remote_docker) build -t $(docker_image_name) .

_docker-run: docker-build
	@echo $(DOCKER_HOST)
	@echo $(remote_docker)
	$(remote_docker) stop $(service_name) || true
	$(remote_docker) rm $(service_name) || true
	$(remote_docker) run -d -p $(DOCKER_SERVICE_PORT):$(DOCKER_SERVICE_PORT) \
		--name $(service_name) \
		--env-file .env \
		--restart=always \
		$(DOCKER_RUN_OPTS) \
		$(docker_image_name)

docker-run-remote:
	REMOTE=true sumake _docker-run

docker-run-local:
	sumake _docker-run

docker-push:
	docker push $(docker_image_name)
