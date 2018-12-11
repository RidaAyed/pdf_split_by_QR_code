#!/usr/bin/env python
# encoding: utf-8

import io, os

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

        self.__split_pages()
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
    def code(file_path=None, mode='Y800', barcode_type='QRCODE'):

        import zbar
        from PIL import Image

        img = Image.open(file_path)
        pil = img.convert('L')
        width, height = pil.size
        try:
            raw = pil.tobytes()
        except AttributeError:
            raw = pil.tostring()

        image = zbar.Image(width, height, mode, raw)
        
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        result = scanner.scan(image)

        barcodes = []
        if result:
            for barcode in image:
                if not barcode_type or str(barcode.type) == barcode_type:
                    barcodes.append(barcode.data.decode(u'utf-8'))

        return barcodes

    def __split_pages(self):
        for count_index, num in enumerate(xrange(self.pages_count), 1):
            self.__pages[num] = self.reader.getPage(num)

            import tempfile

            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                
                wrt = PdfFileWriter()
                wrt.addPage(self.__pages[num])
                wrt.write(tmp)
                tmp.close()

                from wand.image import Image

                with tempfile.NamedTemporaryFile(delete=False) as out:
                    with Image(filename=tmp.name, resolution=300) as img:

                        img.format = 'png'
                        img.save(file=out)
                
                        self.__qrcodes[num] = Tool.code(out.name)
                        
                        os.unlink(out.name)

                os.unlink(tmp.name)
