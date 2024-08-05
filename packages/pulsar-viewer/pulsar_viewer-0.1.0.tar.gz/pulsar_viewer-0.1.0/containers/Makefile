.PHONY: nop
nop:
	@echo Hello!


DOCKER := podman
COMPOSE := $(DOCKER) compose


.PHONY: up
up:
	$(COMPOSE) up -d


.PHONY: down
down:
	$(COMPOSE) down --volumes --remove-orphans


.PHONY: redo
redo:
	$(MAKE) down
	$(MAKE) up


.PHONY: shell
shell:
	$(DOCKER) exec -it pulsar-viewer_pulsar_1 /bin/bash


MSG := {"hello": "world"}
N_MSGS := 1
TOPIC := persistent://public/default/hello1


.PHONY: send-msg
send-msg:
	$(DOCKER) exec pulsar-viewer_pulsar_1 bin/pulsar-client produce -m '$(MSG)' -n $(N_MSGS) $(TOPIC)
