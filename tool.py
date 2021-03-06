#!/usr/bin/env python
# encoding: utf-8

import io, os, uuid
from tempfile import NamedTemporaryFile

import zbar
import zbar.misc
from skimage.io import imread as read_image

from wand.image import Image as WAND_Image

from PyPDF2 import PdfFileReader, PdfFileWriter
from PyPDF2.utils import PdfReadError


class File(object):

    def __init__(self, source, num, folder):
        
        self.num = num
        self.folder = folder
        self.uuid = str(uuid.uuid4())
        
        self.source = source
        self.file_name = "{}_{}.pdf" .format(self.source.filename, self.uuid)

    def save(self, folder=None):
        
        tmpl = "[%s] from file '%s' copy page (%s) to %s"

        page = self.source.reader.getPage(self.num)
        path = os.path.join(folder or self.folder, self.file_name)
        
        try:
            with open(path, 'wb') as output: 
                wrt = PdfFileWriter()
                wrt.addPage(page)
                wrt.write(output)
                return tmpl % ('ok', self.source.source, self.num, path)
        except Exception as ex:
            return tmpl % (ex, self.source.source, self.num, path)


class Tool(object):
    def __init__(self, source=None):
        self.source = source
        self.__pages = {}
        self.__qrcodes = {}

        if not self.source:
            raise ValueError('Source is not set')
        try:
            self.reader = PdfFileReader(open(self.source, "rb"))
        except Exception as er:
            raise ValueError('Is not PDF [%s]' % self.source)
        else:

            head, tail = os.path.split(self.source)
            self.filename = '.'.join(tail.split('.')[:-1])
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
                    raise ValueError('First page is not QRcode')

                __files.append(File(
                    self,
                    num, 
                    folder
                ))
        return __files

    @staticmethod
    def code(file_path=None, barcode_type='QRCODE'):
   
        
        
        image = read_image(file_path)
        
        if len(image.shape) == 3:
            image = zbar.misc.rgb2gray(image)
        
        barcodes = []

        scanner = zbar.Scanner()
        results = scanner.scan(image)
        for barcode in results:
            barcodes.append(barcode.data.decode(u'utf-8'))    
        
            
        return barcodes

    def __split_pages(self):
        for count_index, num in enumerate(range(self.pages_count), 1):
            self.__pages[num] = True
            page = self.reader.getPage(num)

            with NamedTemporaryFile(delete=False) as tmp:
                
                wrt = PdfFileWriter()
                wrt.addPage(page)
                wrt.write(tmp)
                tmp.close()

                with NamedTemporaryFile(delete=False) as out:
                    
                    with WAND_Image(filename=tmp.name, resolution=150) as img:
                        img.format = 'jpg'
                        img.save(file=out)
                    
                    out.close()

                    self.__qrcodes[num] = Tool.code(out.name)

                    os.unlink(out.name)

                os.unlink(tmp.name)
