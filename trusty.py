import os
from os.path import basename
import sys
import yaml
import urllib
from shutil import copyfile, move
import bagit

class Trusty:
    def __init__(self, title):
        self.settings = self.load_settings('./settings.yaml')
        self.title = title
    
        
    def load_settings(self,settings_file):
        """ Load the settings from the settings.yaml file """
        yaml_file = file(settings_file, 'r')
        settings = yaml.load(yaml_file)
        return settings

    def file_list(self,root_directory):
        """ Get a list of files from a root directory """
        file_list = []
        for root, sub_folders, files in os.walk(root_directory):
            for file in files:
                file_list.append(os.path.join(root,file))
        return file_list

    def create_bag_dirs(self,file_list):
        """ Create the directories for the bags -- bagit.py only supports bag in place """
        dir_list = []
        for file in file_list:
            file_name = file.rsplit('/', 1)[-1]
            dirname = self.dir_to_filename(file)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
                copyfile(file,dirname+"/"+file_name)
                print(dirname+"/"+file_name)
                dir_list.append(dirname)
        return dir_list

    def create_bags(self,dir_list):
        """ Actually create the bags and write the APTrust info file """
        for dir in dir_list:
            bag = bagit.make_bag(dir, {'Source-Organization': self.settings[':institution']['source_org'], 'Internal-Sender-Description' :'','Internal-Sender-Identifier':''})
            bag.save(manifests=True)
            self.write_aptrust_info(dir)
            move(dir, self.settings[':local_server']['storage_directory'])

    def write_aptrust_info(self, dir):
        """ Write the aptrust-info.txt file """
        with open(dir+'/aptrust-info.txt', 'w+') as f:
            s = "Title:"+self.title+"\nAccess: Restricted"
            f.write(s)
            f.close
            
    def dir_to_filename(self,filename):
        """ Create a valid APTrust bag name from a file path """
        return self.settings[':institution']['institution']+'.'+basename(filename).replace(" ","_").replace("/","_").replace(".","_")

    def create_aptrust_bags(self):
        dir_list = self.create_bag_dirs(self.file_list(sys.argv[1]))
        print self.file_list(sys.argv[1])
        print dir_list
        self.create_bags(dir_list)
        



