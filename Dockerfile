FROM python:2.7
MAINTAINER Aleksey Molchanov <molchanov.av@gmail.com>

RUN apt-get update && \
    apt-get install -y build-essential libzbar-dev libcairo2-dev libjpeg-dev libpango1.0-dev libgif-dev libpng-dev imagemagick ghostscript libmagickwand-dev zbar-tools zlib1g-dev libzbar-dev libpython-dev 

RUN mkdir -p /opt/
RUN git clone https://github.com/AlekseyMolchanov/pdf_split_by_QR_code.git  /opt/pdf_split_by_QR_code

WORKDIR /opt/pdf_split_by_QR_code
RUN pip install -r requirements.txt

# WORKDIR /ext

ENTRYPOINT [ "pytest" ]
# ENTRYPOINT [ "python", "/opt/pdf_split_by_QR_code/main.py"]