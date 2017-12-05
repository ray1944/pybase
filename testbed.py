import unittest
import partgen as pg

class TestMethods(unittest.TestCase):
    def test_aldparsing(self):
        pg.chtodir()
        pg.init()
        pg.signon()
        print("server id list: ")
        print(pg.getSvrID())
        self.assertEqual(True, True)

if __name__ == '__main__':
    unittest.main()

