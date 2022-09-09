SCRIPTS_DIR=scripts

.PHONY: help
.SILENT:

help: # Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

clean-test-db: # Clean test database.
	ENV="test"; python -m app.clean_test_database

start-test: # Start test.
	bash ./${SCRIPTS_DIR}/test_start.sh

start-dev-server: # Start development server.
	bash ./${SCRIPTS_DIR}/start_dev_server.sh

init-dev-db: # Init development database.
	bash ./${SCRIPTS_DIR}/dev_database_init.sh

load-env: # Load environment variable from .env file.
	if [ -f ".env" ]; then \
		export $(cat .env | xargs); \
	else \
		echo "The .env file doesn't exist."; \
	fi

freeze: # Export the requirements.txt file.
	poetry export --without-hashes -f requirements.txt --output requirements.txt

gen-openapi-json: # Generate openapi.json in assets.
	python app/generate_openapi_json.py

gen-secret: # Generate random secret.
	openssl rand -base64 32
