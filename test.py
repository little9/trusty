import unittest
from trusty import Trusty
import bagit
import shutil

class TestTrustyFunctions(unittest.TestCase):
    def test_settings(self):
        t = Trusty({'title':'Title','description':'A description','access':'Restricted'})
        self.assertEqual(t.settings[':institution']['institution'], 'example.edu')

    def test_file_list(self):
        t = Trusty({'title':'Title','description':'A description','access':'Restricted'})
        file_list = t.file_list('.')
        self.assertTrue('./settings.yaml' in file_list)
        
    def test_create_aptrust_bags(self):
        t = Trusty({'title':'Title','description':'A description','access':'Restricted'})
       
        t.settings[':local_server']['storage_directory'] = './test_storage'
        t.create_aptrust_bags('./test_data')
        bag = bagit.Bag('./test_storage/example.edu.test_txt/')
        self.assertTrue(bag.validate, True)
        shutil.rmtree('./test_storage/example.edu.test_txt/')

if __name__ == '__main__':
    unittest.main()
    
