.PHONY: devbuild
devbuild:
	docker-compose -f docker-compose.dev.yaml build

.PHONY: devrun
devrun:
	docker-compose -f docker-compose.dev.yaml up

.PHONY: imagesbuild
imagesbuild:
	docker build -t security-gym-python -f images/python/Dockerfile .

.PHONY: prodbuild
prodbuild:
	docker-compose -f docker-compose.prod.yaml build

.PHONY: prodrun
prodrun:
	docker-compose -f docker-compose.prod.yaml up
