import unittest
from wareHouse import wareHouse


class TestWareHouseDetails(unittest.TestCase):

    def test_addItemFailure(self):
        self.wareHouse = wareHouse()
        # Test Invalid data cases
        return_result = self.wareHouse.incrementItem('tv', 'TV')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1.', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('TV', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('@', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem(' 1', '@')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1 ', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem(1.2, 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('wh1', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH1', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2: !', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH@: 1.2', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2: 1', '*')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2:1 ', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem('*', ' 1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem(' 1', '1 ')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1 ', 1)
        assert False == return_result

        return_result = self.wareHouse.incrementItem(1.2, 'tv')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('tv', '1.')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1.', 'TV')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('TV', '@')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('@', ' 1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem(' 1', '1 ')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1 ', 1.2)
        assert False == return_result

        return_result = self.wareHouse.incrementItem(1.2, 'wh1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('wh1', 'WH1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH1', 'WH2')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2', 'WH2: !')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2: !', 'WH@: 1.2')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH@: 1.2', 'WH2: 1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2: 1', 'WH2:1 ')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('WH2:1 ', '1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('*', '*')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('', '')
        assert False == return_result

        return_result = self.wareHouse.incrementItem(' 1', ' 1')
        assert False == return_result

        return_result = self.wareHouse.incrementItem('1 ', '1 ')
        assert False == return_result

        return_result = self.wareHouse.incrementItem(1.2, 1.2)
        assert False == return_result

    def test_addItemSuccess(self):
        self.wareHouse = wareHouse()

        # Test Valid data cases
        return_result = self.wareHouse.incrementItem(1, 1)
        assert True == return_result

        # Test Valid data cases
        return_result = self.wareHouse.incrementItem(2, 12)
        assert True == return_result

        # Test Valid data cases
        return_result = self.wareHouse.incrementItem(3, 140)
        assert True == return_result

        # Test Valid data cases
        return_result = self.wareHouse.incrementItem(4, 1001)
        assert True == return_result

