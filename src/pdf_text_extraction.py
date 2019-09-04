# -*-coding:utf-8 -*-

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTPage, LTChar, LTAnno, LAParams, LTTextBox, LTTextLine
from dateutil.parser import parse
import time
import csv, os


class PDFPageDetailedAggregator(PDFPageAggregator):
    def __init__(self, rsrcmgr, pageno=1, laparams=None):
        PDFPageAggregator.__init__(self, rsrcmgr, pageno=pageno, laparams=laparams)
        self.rows = []
        self.page_number = 0

    def receive_layout(self, ltpage):
        def render(item, page_number):
            if isinstance(item, LTPage) or isinstance(item, LTTextBox):
                for child in item:
                    render(child, page_number)
            elif isinstance(item, LTTextLine):
                child_str = ''
                for child in item:
                    if isinstance(child, (LTChar, LTAnno)):
                        child_str += child.get_text()
                child_str = ' '.join(child_str.split()).strip()
                if child_str:
                    row = (page_number, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3],
                           child_str)  # bbox == (x1, y1, x2, y2)
                    self.rows.append(row)
                for child in item:
                    render(child, page_number)
            return

        render(ltpage, self.page_number)
        self.page_number += 1
        self.rows = sorted(self.rows, key=lambda x: (x[0], -x[2]))
        self.result = ltpage


class PdfExtractor:
    def __init__(self):
        self.a=1

    def get_pdf_text(self,pdf_path):
        open_file = open(pdf_path, 'rb')
        parser = PDFParser(open_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageDetailedAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            # receive the LTPage object for this page
            device.get_result()
        device_data_list = device.rows
        # print(device_data_list)
        device_data_list = ' '.join([i[-1] for i in device_data_list])
        # print(device_data_list)
        open_file.close()
        return device_data_list


if __name__ == "__main__":
    obj = PdfExtractor()
    data_list = obj.get_pdf_text("doc_file/90378400.pdf")
    print(data_list)