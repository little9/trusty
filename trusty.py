 # -*- coding: utf-8 -*-
import os
from os.path import basename
import sys
import yaml
import urllib
from shutil import copyfile, move, copytree
import bagit
import logging

class Trusty(object):
    def __init__(self, collection_meta):
        self.settings = self.load_settings('./settings.yaml')
        self.title = collection_meta['title']
        self.access = collection_meta['access']
        self.description = collection_meta['description']
        self.remove_sub_dir = collection_meta['subdir']
        self.original_root = self.settings[':local_server']['storage_root']
        self.logging = logging.getLogger()
        
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
                if self.settings[':local_server']['ignore'] not in file:
                    file_list.append(os.path.join(root,file))
        return file_list

    def create_bag_dirs(self,file_list):
        """ Create the directories for the bags -- bagit.py only supports bag in place """
        dir_list = []
        for file in file_list:
            sub_dirs = self.sub_dirs(file)
            file_name = file.rsplit('/', 1)[-1]
           
            dirname = self.dir_to_filename(file)
    
            if not os.path.exists(dirname):
                os.makedirs(dirname+"/"+sub_dirs)
                copyfile(file,dirname+"/"+sub_dirs+"/"+file_name)
                dir_list.append(dirname+sub_dirs)
                print dir_list
        return dir_list

    def create_bags(self,dir_list):
        """ Actually create the bags and write the APTrust info file """
        for dir in dir_list:
            dir = dir.split('/')[0]
            bag = bagit.make_bag(dir, {'Source-Organization': self.settings[':institution']['source_org'], 'Internal-Sender-Description' :'','Internal-Sender-Identifier':''})
            bag.save(manifests=True)
            self.write_aptrust_info(dir)
            move(dir, self.settings[':local_server']['storage_directory'])

    def write_aptrust_info(self, dir):
        """ Write the aptrust-info.txt file """
        with open(dir+'/aptrust-info.txt', 'w+') as f:
            s = "Title: "+self.title+"\n"+"Description: "+self.description+"\nAccess: "+self.access
            f.write(s)
            f.close
            
    def dir_to_filename(self,filename):
        """ Create a valid APTrust bag name from a file path """
        if self.remove_sub_dir:
            new_filename = filename.replace(self.remove_sub_dir,'')
            dir_filename = self.settings[':institution']['institution']+'.'+new_filename[2:].replace(" ","_").replace("/","_").replace(".","_")
        else:
            
            dir_filename = self.settings[':institution']['institution']+'.'+basename(filename).replace(" ","_").replace("/","_").replace(".","_")
        return dir_filename 


    def create_aptrust_bags(self,src):
        """ Create APTrust bags for all files in a directory """
        dir_list = self.create_bag_dirs(self.file_list(src))
        self.create_bags(dir_list)

    def create_aptrust_metadata_bag(self, src,storage_dir):
        no_root_dir = src.replace(storage_dir,'')
        dirname ='miami.edu.'+no_root_dir
        copytree(src, dirname)
        bag = bagit.make_bag(dirname, {'Source-Organization': self.settings[':institution']['source_org'], 'Internal-Sender-Description' :'','Internal-Sender-Identifier':''})
        bag.save(manifests=True)
        self.write_aptrust_info(dirname)
        move(dirname, self.settings[':local_server']['storage_directory'])
       
    def sub_dirs(self, filepath):
        """ Given an absolute filepath, return all the subdirectories, if you don't want some subdirs, you can pass a parameters when creating an instance of the class and it will be removed """
        dir_list = os.path.abspath(filepath).rsplit('/')
        dir_list.pop()
        dir_list.pop(0)
        join_dir_list = "/".join(dir_list)
        if self.remove_sub_dir:
            new_dir_list = join_dir_list.replace(self.remove_sub_dir,'')
        else:
            new_dir_list = join_dir_list
            
        return "/" + new_dir_list

