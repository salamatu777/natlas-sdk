.PHONY: install test serve docker-build docker-run

install:
	pip install -e .[all]

test:
	pytest tests/

serve:
	natlas serve --port 8000

docker-build:
	docker build -t natlas-api .

docker-run:
	docker-compose up --build
