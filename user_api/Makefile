GIT_CURRENT_BRANCH := ${shell git symbolic-ref --short HEAD}

.PHONY: help clean test run

.DEFAULT: help

help:
	@echo "make clean:"
	@echo "       Removes all pyc, pyo and __pycache__"
	@echo ""
	@echo "make setup"
	@echo "       Install dependencies"
	@echo "       set virtualenv on this path"
	@echo ""
	@echo "make test:"
	@echo "       Run tests with pytest(necessary databases ON)"
	@echo ""
	@echo "make docker:"
	@echo "       Run app with docker and docke-compose"
	@echo ""
	@echo "make dockerdown:"
	@echo "       Remove app from docker with docke-compose down"
	@echo ""
	@echo "make rundev:"
	@echo "       Run the web application(necessary databases ON)"
	@echo ""

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . | grep -E "__pycache__|.pytest_cache|.pyc|.DS_Store$$" | xargs rm -rf

setup:
	@echo "---- Setting Enviroment ----"
	@virtualenv env
	@. env/bin/activate
	@echo "---- Installing Python dependencies ----"
	@pip3 install -r requirements.txt --upgrade

test:
	@pytest --verbose --disable-pytest-warnings --color=yes tests/

docker:
	@echo "---- Building & Up Containers ----"
	@docker-compose down
	@docker-compose build
	@docker-compose up -d	
	@sleep 5
	@echo "---- Acess http://127.0.0.1:8080/api-docs ----"

dockerdown:
	@docker-compose down

rundev:
	python3 app.py