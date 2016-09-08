import os
import sys
import yaml
import urllib
from shutil import copyfile
import bagit

class Trusty:
    def __init__(self, title):
        self.global_settings = self.settings('./settings.yaml')
        self.title = title
        
    def settings(self,settings_file):
        yaml_file = file(settings_file, 'r')
        settings = yaml.load(yaml_file)
        return settings

    def file_list(self,root):
        file_list = []
        for root, sub_folders, files in os.walk(root):
            for file in files:
                file_list.append(os.path.join(root,file))
        return file_list

    def create_bag_dirs(self,file_list):
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
        for dir in dir_list:
           bag = bagit.make_bag(dir, {'Source-Organization': self.global_settings['institution']['source_org'], 'Internal-Sender-Description' :'','Internal-Sender-Identifier':''})
           bag.save(manifests=True)
           self.write_aptrust_info(dir)

    def write_aptrust_info(self, dir):
         with open(dir+'/aptrust-info.txt', 'w+') as f:
               s = "Title:"+self.title+"\nAccess: Restricted"
               f.write(s)
               f.close
               
    def dir_to_filename(self,filename):
        return t.global_settings['institution']['institution']+'.'+filename.replace(" ","_").replace("/","_").replace(".","_")

t = Trusty()
dir_list = t.create_bag_dirs(t.file_list(t.global_settings['local_server']['storage_directory']))
t.create_bags(dir_list)

