.PHONY: createsuperuser
createsuperuser:
	uv run server/manage.py createsuperuser

.PHONY: makemigrations
makemigrations:
	uv run server/manage.py makemigrations

.PHONY: migrate
migrate:
	uv run server/manage.py migrate

.PHONY: runserver
runserver:
	uv run server/manage.py runserver


.PHONY: update
update:
	git pull
	uv sync --no-dev
	uv run server/manage.py migrate


.PHONY: g-add
g-add:
	isort .
	black .
	git add .

# I used these "@" to hide them in console
.PHONY: check-project
check-project:
	@echo "\033[36mRunning Black to format python code...\033[0m"
	@black .
	@echo "\033[32mNow running flake8...\033[0m"
	@uv run flake8 . && echo "\033[32m✓ Flake8 check completed!\033[0m" || (echo "\033[31m✗ Flake8 found issues!\033[0m" && exit 1)


.PHONY: pre-commit-boiler
pre-commit-boiler:
	uv run pre-commit sample-config

.PHONY: run-pre-commit
run-pre-commit: g-add
	uv run pre-commit run --all-files;

.PHONY: shell
shell:
	uv run server/manage.py shell