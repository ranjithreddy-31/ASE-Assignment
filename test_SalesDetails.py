import unittest
from salesDetails import SalesDetails
import pandas as pd

class TestSalesDetails(unittest.TestCase):
    def test_getDataframe(self):
        self.salesDetails = SalesDetails()
        # Test invalid filepath case 
        assert pd.DataFrame().equals(self.salesDetails.getDataframe('test'))

    def test_generateInvoiceFailure(self):
        self.salesDetails = SalesDetails()
        # Test Invalid data cases
        return_result = self.salesDetails.generateInvoice('test',1,1,1)
        assert False == return_result

        return_result = self.salesDetails.generateInvoice(1,'test',1,1)
        assert False == return_result

        return_result = self.salesDetails.generateInvoice(1,1,'test',1)
        assert False == return_result

        return_result = self.salesDetails.generateInvoice(1,1,1,'test')
        assert False == return_result

        return_result = self.salesDetails.generateInvoice(100,1,1,0)
        assert False == return_result

        return_result = self.salesDetails.generateInvoice(1,3,1,0)
        assert False == return_result
    
    def test_generateInvoiceSuccess(self):
        self.salesDetails = SalesDetails()

        # Test Valid data cases
        return_result = self.salesDetails.generateInvoice(1,1,1,0)
        assert True == return_result

        return_result = self.salesDetails.generateInvoice(1,2,1,0)
        assert True == return_result

        return_result = self.salesDetails.generateInvoice(1,1,1,1)
        assert True == return_result

        return_result = self.salesDetails.generateInvoice(1,2,2,1)
        assert True == return_result

    def test_joinDataframes(self):
        self.salesDetails = SalesDetails()
        # Test both dataframes empty case
        first = pd.DataFrame()
        second = pd.DataFrame()
        assert pd.DataFrame().equals(self.salesDetails.joinDataframes(first,second))

        # Test second dataframe empty case
        first = pd.DataFrame({
            'Column_1' : ['A', 'B'],
            'Column_2' : [1,2]
        })
        second = pd.DataFrame()
        assert first.equals(self.salesDetails.joinDataframes(first,second))
        # Test first dataframe empty case
        first = pd.DataFrame()
        second = pd.DataFrame({
            'Column_1' : ['A', 'B'],
            'Column_2' : [1,2]
        })
        # Test both dataframes valid case
        assert second.equals(self.salesDetails.joinDataframes(first,second))
        first = pd.DataFrame({
            'Column_1' : ['A', 'B'],
            'Column_2' : [1,2]
        })
        second = pd.DataFrame({
            'Column_1' : ['C', 'D'],
            'Column_2' : [3,4]
        })

        expected_result = pd.DataFrame({
            'Column_1' : ['A','B','C','D'],
            'Column_2' : [1,2,3,4]
        })

        assert expected_result.equals(self.salesDetails.joinDataframes(first,second))

    def test_payInstallmentFailure(self):
        self.salesDetails = SalesDetails()

        # Test Invalid data cases
        assert False == self.salesDetails.payInstallment(None,None)
        assert False == self.salesDetails.payInstallment(None,10)
        assert False == self.salesDetails.payInstallment(1,None)

        assert False == self.salesDetails.payInstallment('testVar1','testVar2')
        assert False == self.salesDetails.payInstallment('testVar1',10)
        assert False == self.salesDetails.payInstallment(1,'testVar2')

        invalid_invoice_id = -100   
        assert False == self.salesDetails.payInstallment(invalid_invoice_id,10)

    def test_payInstallmentSuccess(self):
        self.salesDetails = SalesDetails()
        # Test valid data cases
        assert True == self.salesDetails.payInstallment(1,1)
        assert True == self.salesDetails.payInstallment(2,2)

    def test_closeInvoiceFailure(self):
        self.salesDetails = SalesDetails()
        # Test invalid data cases
        assert False == self.salesDetails.closeInvoice()
        assert False == self.salesDetails.closeInvoice('testVariable')
        assert False == self.salesDetails.closeInvoice(0)
        assert False == self.salesDetails.closeInvoice(-100)

    def test_closeInvoiceSuccess(self):
        self.salesDetails = SalesDetails()
        # Test Valid data case
        assert True == self.salesDetails.closeInvoice(1)

    def test_showOpenInvoices(self):
        self.salesDetails = SalesDetails()
        # Test showOpenInvoices success case
        assert True == self.salesDetails.showOpenInvoices()

    def test_showClosedInvoices(self):
        self.salesDetails = SalesDetails()
        # Test showClosedInvoices success case
        assert True == self.salesDetails.showClosedInvoices()
