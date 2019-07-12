.PHONY: devbuild
devbuild:
	docker build -t security-gym-python -f images/python/Dockerfile .
	docker-compose -f docker-compose.dev.yaml build

.PHONY: devrun
devrun:
	docker-compose -f docker-compose.dev.yaml up
