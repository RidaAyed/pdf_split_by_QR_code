sample:
	python main.py ./sample.pdf

test:
	pytest -vs

build:
	docker build --rm -f "Dockerfile" -t pdf_qr_code_split:latest .

docker_test:
	docker run -it --rm pdf_qr_code_split
	
docker_sample:	
	docker run -it  --rm -v $(pwd):/ext --entrypoint "python" pdf_qr_code_split main.py ./sample.pdf

work:
	docker run -it  --rm \
			-v /home/ra/Dropbox:/dropbox \
			-v /home/ra/sources:/sources \
			--entrypoint "python" pdf_qr_code_split main.py /sources/sample.pdf