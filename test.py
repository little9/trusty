 # -*- coding: utf-8 -*-
import unittest
from trusty import Trusty
import bagit
import shutil

class TestTrustyFunctions(unittest.TestCase):
           
    def test_create_aptrust_bags(self):
        t = Trusty({'title':'Title','description':'A description','access':'Restricted','subdir':''})
        t.settings[':institution']['institution'] = 'example.edu'
        t.settings[':local_server']['storage_directory'] = './test_storage'
        t.create_aptrust_bags('./test_data')
        bag = bagit.Bag('./test_storage/example.edu.test_txt/')
        self.assertTrue(bag.validate, True)
        shutil.rmtree('./test_storage/example.edu.test_txt/')

if __name__ == '__main__':
    unittest.main()
    
