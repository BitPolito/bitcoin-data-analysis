frontend:
	poetry run streamlit run dashboard/On-chain.py

test:
	pytest tests/
	
isort:
	poetry run isort --profile black . 

black:
	poetry run black . 

format:
	make isort
	make black
	make mypy

mypy:
	poetry run mypy bitdata --ignore-missing

clean:
	rm -r bitdata.egg-info/ || true
	find . -name ".DS_Store" -exec rm -f {} \; || true
	rm -rf dist || true
	rm -rf build || true
	
package:
	poetry export -f requirements.txt --without-hashes --output requirements.txt
	make clean
	python setup.py sdist bdist_wheel
	
test:
	pytest tests/
	
install:
	make clean
	python setup.py sdist bdist_wheel
	pip install --upgrade dist/* 

upload:
	make clean
	python setup.py sdist bdist_wheel
	twine upload --repository pypi dist/*

docker-build:
	docker build -t bitdata .

docker-run:
	docker run -p 8501:8501 -v ./frontend:/app/frontend bitdata

docker-stop:
	-docker stop bitdata
	-docker rm bitdata

docker:
	-make docker-stop
	-make docker-build
	-make docker-run
