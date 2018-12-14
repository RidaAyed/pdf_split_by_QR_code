sample:
	python main.py ./sample.pdf

test:
	pytest -vs

build:
	docker build --rm -f "Dockerfile" -t pdf_qr_code_split:latest .

docker_test:
	docker run -it --rm pdf_qr_code_split
	
docker_sample:
	docker run -it --rm --entrypoint "python main.py ./sample.pdf" pdf_qr_code_split
	
