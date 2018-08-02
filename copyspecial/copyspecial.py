#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import commands
from zipfile import *

"""Copy Special exercise
"""

# +++your code here+++
# Write functions and modify main() to call them
def check_special(dir_path):

	path = os.listdir(dir_path)
	filenames = []
	
	for i in path:
		file_name = re.search('__\w*__|__\w*\W*\w*__',i)
		if file_name:
			filenames.append(i)

	return filenames

def copy_special(filenames, todir_path, fromdir_path):

#	print filenames	
	saved_path = os.getcwd()

	os.chdir(fromdir_path)
	src_path = os.getcwd()

	os.chdir(todir_path)
	des_path =  os.getcwd()	

	for f in filenames:
		new_file_names = os.path.join(src_path, f)
		if (os.path.isfile(new_file_names)):
			shutil.copy(new_file_names, des_path)
	os.chdir(saved_path)

def zip_special(filenames, tozip_path):

	os.chdir(tozip_path)
	zip_path = os.getcwd()
	
	zipname = 'files.zip'
#	zip_file = ZipFile(zipname,'w')

	with ZipFile(zipname,'w') as z:	
		for i in filenames:
			new_file = os.path.join(zip_path,i)
			if os.path.isfile(new_file):
				z.write(i)
			else:
				print i,"=> FILE DOES NOT EXIST"

def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print "usage: [--todir dir][--tozip zipfile] dir [dir ...]";
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  tozip = ''
  if args[0] == '--tozip':
    tozip = args[1]
    del args[0:2]

  if len(args) == 0:
    print "error: must specify one or more dirs"
    sys.exit(1)

  # +++your code here+++
  # Call your functions
  filenames = check_special(args[0])
  if todir:
    copy_special(filenames, todir, args[0])
  if tozip:
    zip_special(filenames, tozip)

if __name__ == "__main__":
  main()
