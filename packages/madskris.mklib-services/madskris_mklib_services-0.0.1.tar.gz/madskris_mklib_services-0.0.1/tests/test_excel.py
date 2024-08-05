from src.mklib_services.excel import *

class TestExcel:

    def testReadExcelFile(self):
        result = readExcelFile("TestExcel.xlsx")
        
        if result.successful:
            return
        
        raise AssertionError(result)
    
    def testReadMateriell(self):
        result = readMateriell()

        if result.successful:
            return

        raise AssertionError(result)

    def testGetMateriell(self):

        result = getMateriell()
        
        if result.successful:
            return
        
        raise AssertionError(result)
    
    def testReadProdukter(self):
        result = readProdukter()
        
        if result.successful:
            return

        raise AssertionError(result)
    
    def testGetProdukter(self):
        result = getProdukter()
        
        if result.successful:
            return
        
        raise AssertionError(result)

    def testReadPriser(self):
        result = readPriser()
        
        if result.successful:
            return
        
        raise AssertionError(result)

    def testGetPriser(self):
        result = getPriser()
        
        if result.successful:
            return
        
        raise AssertionError(result)

    def testReadOpitel(self):
        result = readOpitel()
        
        if result.successful:
            return

        raise AssertionError(result)
    
    def testGetOpitel(self):
        result = getOpitel()
        
        if result.successful:
            return
        
        raise AssertionError(result)