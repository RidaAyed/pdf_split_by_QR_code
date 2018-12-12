sample:
	./main.py ./sample.pdf

build:
	docker build --rm -f "Dockerfile" -t pdf_qr_code_split:latest .

test:
	docker run -it --rm  pdf_qr_code_split
	# docker run -it --rm -v $(pwd):/ext pdf_qr_code_split sample.pdf
