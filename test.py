import unittest
from trusty import Trusty

class TestTrustyFunctions(unittest.TestCase):
   
    def test_settings(self):
        t = Trusty()
        self.assertEqual(t.settings('settings.yaml')[':institution'][':institution'], 'example.edu')

    def test_file_list(self):
        t = Trusty()
        file_list = t.file_list('.')
        self.assertTrue('./settings.yaml' in file_list)
    
        
if __name__ == '__main__':
    unittest.main()
    
