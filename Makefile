.PHONY: install test lint format build local plan deploy-dev destroy

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	pytest -q

lint:
	ruff --fix src || true
	black .
	ruff .

format:
	black .

build:
	# Build deployment packages for Lambdas (placeholder, see per-lambda README)
	@echo "Build completed"

local:
	docker-compose up --build

plan:
	cd terraform/environments/dev && terraform init && terraform plan

deploy-dev:
	cd terraform/environments/dev && terraform apply

destroy:
	cd terraform/environments/dev && terraform destroy -auto-approve
