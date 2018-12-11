#!/usr/bin/env python
# encoding: utf-8

import io, os, uuid

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.utils import PdfReadError


class File(object):
    def __init__(self, source_filename, num, folder, page):
        
        self.num = num
        self.page = page
        self.folder = folder
        
        self._source_filename = source_filename
        self._uuid = str(uuid.uuid4())
        
        self.file_name = "{}_{}" .format(self._source_filename, self._uuid)



class Tool(object):
    def __init__(self, source=None):
        self.source = source
        self.__pages = {}
        self.__qrcodes = {}

        import os
        head, tail = os.path.split(self.source)

        self.source_filename = '.'.join(tail.split('.')[:-1])
        

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

    @property
    def files(self):
        __files = []

        folder = None

        for num in self.__pages.keys():
            barcodes = self.__qrcodes.get(num)
            if barcodes:
                folder = barcodes[0]
            else:
                if not folder:
                    raise StandardError('First page is not QRcode')

                __files.append(File(
                    self.source_filename,
                    num, 
                    folder,
                    self.__pages.get(num)
                ))
        return __files

    @staticmethod
    def code(file_path=None, barcode_type='QRCODE'):

        import zbar
        from PIL import Image

        pil = Image.open(file_path).convert('L')        
        width, height = pil.size

        try:
            raw = pil.tobytes()
        except AttributeError:
            raw = pil.tostring()

        image = zbar.Image(width, height, 'Y800', raw)
        
        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')
        result = scanner.scan(image)

        barcodes = []

        if result == 0: 
            pass
        else:
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
                    
                    with Image(filename=tmp.name, resolution=150) as img:
                        img.format = 'jpg'
                        img.save(file=out)
                    
                    out.close()

                    self.__qrcodes[num] = Tool.code(out.name)

                    os.unlink(out.name)

                os.unlink(tmp.name)
