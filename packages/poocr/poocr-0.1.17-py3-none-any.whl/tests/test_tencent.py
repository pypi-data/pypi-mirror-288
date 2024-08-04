import unittest

from poocr.api.ocr2excel import *


class TestTencent(unittest.TestCase):

    def setUp(self):
        self.SecretId = 'AKIDshNuIVZUE6pOoARZWJvQq8GC2qqeOwHP'
        self.SecretKey = 'NeEc6WsKn7HI8rOjrpbBbfcN3Xp6GFTv'

    def test_vin_ocr(self):
        r = VatInvoiceOCR(id=self.SecretId, key=self.SecretKey, img_path=r'./test_files/发票/img.png')
        print(r)

    def test_idcard_ocr(self):
        res = IDCardOCR(
            img_path=r'C:\Users\Lenovo\Desktop\temp\正面.jpg')
        print(res)

    def test_VatInvoiceOCR2Excel(self):
        VatInvoiceOCR2Excel(input_path=r'./test_files/发票/img.png',
                            output_excel=r'./VatInvoiceOCR2Excel.xlsx',
                            id=self.SecretId, key=self.SecretKey)

    def test_TrainTicketOCR2Excel(self):
        TrainTicketOCR2Excel(input_path='', output_excel='', configPath='fdasf')

    def test_BizLicenseOCR(self):
        res = poocr.ocr.BizLicenseOCR(img_path=r'./test_files/biz_img/demo1.png', id=self.SecretId, key=self.SecretKey)
        print(res)

    def test_IDCardOCR2Excel(self):
        poocr.ocr2excel.IDCardOCR2Excel(input_path=r'./test_files/', id=self.SecretId, key=self.SecretKey)

    def test_BizLicenseOCR2Excel(self):
        poocr.ocr2excel.BizLicenseOCR2Excel(input_path=r'./test_files/biz_img/', id=self.SecretId, key=self.SecretKey)
