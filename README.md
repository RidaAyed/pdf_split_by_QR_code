# Split PDF document into pages by QR code
Small tool to split pdf document into pages by QR code

[![CircleCI](https://circleci.com/gh/AlekseyMolchanov/pdf_split_by_QR_code/tree/master.svg?style=svg)](https://circleci.com/gh/AlekseyMolchanov/pdf_split_by_QR_code/tree/master)


# Usage

all commands available in Makefile


Use this script as:

  ./main.py <source file path>

Example:

  ./main.py sample.pdf


# Tests
  
  pytest -vs
  
  
#Docker

  build:
  
  docker build --rm -f "Dockerfile" -t pdf_qr_code_split:latest .

  run tests:
  
  docker run -it --rm pdf_qr_code_split
  
  run sample:
  docker run -it --rm --entrypoint "python main.py ./sample.pdf" pdf_qr_code_split





  
