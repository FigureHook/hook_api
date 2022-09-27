SCRIPTS_DIR=scripts

.PHONY: help
.SILENT:

help: # Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

start-test: # Start test.
	bash ./${SCRIPTS_DIR}/test_start.sh

dev-server: # Start development server.
	bash ./${SCRIPTS_DIR}/start_dev_server.sh

load-env: # Load environment variable from .env file.
	if [ -f ".env" ]; then \
		export $(cat .env | xargs); \
	else \
		echo "The .env file doesn't exist."; \
	fi

freeze: # Export the requirements.txt file.
	poetry export --without-hashes -f requirements.txt --output requirements.txt

openapi-json: # Generate openapi.json in assets.
	python -m app.generate_openapi_json

secret: # Generate random secret.
	openssl rand -base64 32

scripts-executable: # Modify files' permissions in scripts.
	chmod -R +x ${SCRIPTS_DIR}

dev-env-file: # Generate dev.env file.
	bash ./${SCRIPTS_DIR}/generate_env_file.sh

dev-environment: dev-env-file # Initialize development environment.
	bash ./${SCRIPTS_DIR}/init_dev_environment.sh
