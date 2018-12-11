#!/usr/bin/env python
# encoding: utf-8

import io

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.utils import PdfReadError


class Tool(object):
    def __init__(self, source=None):
        self.source = source
        self.__pages = {}
        self.__qrcodes = {}

        if not self.source:
            raise ValueError('Empty input')
        try:
            self.reader = PdfFileReader(file(self.source, "rb"))
        except Exception as er:
            raise StandardError('Is not PDF')

        # self.__split()
        return super(Tool, self).__init__()

    @property
    def pages_count(self):
        return self.reader.getNumPages()

    @property
    def pages(self):
        return self.__pages.values()

    @property
    def qrcodes(self):
        return sum(self.__qrcodes.values(), [])

    @staticmethod
    def pdf_to_image(page, filetype="PNG", resolution = 72,):

        from wand.image import Image

        tmp = PdfFileWriter()
        tmp.addPage(page)


        from pdf2image import convert_from_bytes
        
        
        wrt = PdfFileWriter()
        wrt.addPage(page)

        r = io.BytesIO()
        wrt.write(r)

        images = convert_from_bytes(r.getvalue())
        images[0].save("1.png")


        return img

    @staticmethod
    def code(file_path=None, img=None, mode='Y800', barcode_type='QRCODE'):

        # import zbar

        # img = img or Image.open(file_path)

        # scanner = zbar.ImageScanner()

        # scanner.parse_config('enable')

        # pil = img.convert('L')
        # width, height = pil.size
        # try:
        #     raw = pil.tobytes()
        # except AttributeError:
        #     raw = pil.tostring()

        # image = zbar.Image(width, height, mode, raw)
        # result = scanner.scan(image)

        barcodes = []
        # if result:
        #     for barcode in image:
        #         if not barcode_type or str(barcode.type) == barcode_type:
        #             barcodes.append(barcode.data.decode(u'utf-8'))

        return barcodes

    # def __split(self):
    #     for count_index, num in enumerate(xrange(self.pages_count), 1):
            
    #         page = self.__pages[num] = self.reader.getPage(num)
    #         self.__qrcodes[num] = Tool.code(Tool.pdf_to_image(page))
