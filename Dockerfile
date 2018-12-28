FROM base/archlinux
MAINTAINER Aleksey Molchanov <molchanov.av@gmail.com>

RUN pacman -Syu --noconfirm
RUN pacman -S git file awk gcc --noconfirm
RUN pacman -S python python-pip --noconfirm
RUN pacman -S base-devel --noconfirm
RUN pacman -S zbar --noconfirm
RUN pacman -S ghostscript --noconfirm
RUN pacman -S python-wand --noconfirm

RUN echo '<policy domain="coder" rights="read|write" pattern="PDF" />' >> /etc/ImageMagick-6/policy.xml

RUN mkdir -p /opt/
RUN git clone https://github.com/RidaAyed/pdf_split_by_QR_code.git  /opt/pdf_split_by_QR_code
WORKDIR /opt/pdf_split_by_QR_code
RUN pip install -r requirements.txt

ENTRYPOINT [ "pytest" ]