#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import webbrowser
import time

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
	"""Returns a list of the puzzle urls from the given log file,
	extracting the hostname from the filename itself.
	Screens out duplicate urls and returns the urls sorted into
	increasing order."""
	# +++your code here+++
	urls, final_urls, f_url = [], [], []
	d = {}
	with open(filename,'r') as fh:
		all_urls = fh.readlines()

	for i in all_urls:
		test = re.search('\w*/puzzle/\w*',i)
		if test:
			urls.append(i)

	for i in urls:
		test = re.search('/\S*',re.search('GET\s\S*',i).group()).group()
		if test:
			final_urls.append('http://code.google.com/' + test)

	for i in final_urls:
		d[i] = re.search('-\w\w\w\w.jpg',i).group()

	d2 = sorted(d.items(), key=lambda x : x[1])

	for x in d2:
		f_url.append(x[0])
	return f_url


def download_images(img_urls, dest_dir, file_name):
	"""Given the urls already in the correct order, downloads
	each image into the given directory.
	Gives the images local filenames img0, img1, and so on.
	iCreates an index.html in the directory
	with an img tag to show each local image file.
	Creates the directory if necessary.
	"""
	# +++your code here+++
	full_names = []
	animal_dir = 'animal_images'
	place_dir = 'place_code_images'
	html_code1 = """ <html>
				<head><title>index page</title></head>
				<body>"""
	html_code2 = []
	html_code3 = """	
				</body>
			</html>
			"""
	for i in range(0,len(img_urls)):
		full_names.append('img' + str(i) + '.jpg')
	
	os.chdir(dest_dir)
	saved_path = os.getcwd()
	
	if not os.path.exists(animal_dir):
		os.makedirs(animal_dir)
	elif not os.path.exists(place_dir):
		os.makedirs(place_dir)	

	if file_name == 'animal_code.google.com':
		os.chdir(saved_path + '/' + animal_dir)
	
	if file_name == 'place_code.google.com':
		os.chdir(saved_path + '/' + place_dir)

	for i in range(0,len(img_urls)):
		print "Downloading... " + img_urls[i] + " AS " + full_names[i]
		urllib.urlretrieve(img_urls[i],full_names[i])

	imgs = []
	img_path = os.listdir(os.getcwd())
	for i in img_path:
		test = re.match('img\S*',i)
		if test:
			imgs.append(test.group())

	for i in range(0,len(imgs)):
		if file_name == 'animal_code.google.com':
			html_code2.append('<img src="'+ animal_dir + '/img' + str(i) + '.jpg">' )
		if file_name == 'place_code.google.com':
			html_code2.append('<img src="' + place_dir + '/img' + str(i) + '.jpg">' )

	os.chdir(saved_path)	
	with open('index.html','w') as fh:
		fh.write("")
		fh.write(html_code1 + ''.join(html_code2) + html_code3)

	time.sleep(2)
	webbrowser.open("file://" + os.getcwd() +"/index.html")
	

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir, args[0])
  else:
    print '\n'.join(img_urls)

if __name__ == '__main__':
  main()
