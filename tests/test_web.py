# This file is part of python-markups test suite
# License: BSD
# Copyright: (C) Dmitry Shachnev, 2012

import markups.web
import os
import difflib
import sys

def test_web():
	if os.path.exists('tests/data'):
		working_dir='tests/data'
	elif os.path.exists('data'):
		working_dir='data'
	else:
		sys.exit('Could not find data directory!')
	app_data = ('test', '1.0', 'http://example.com/')
	lib = markups.web.WebLibrary(working_dir, app_data)
	lib.update('page.rst')
	expected_file = open(working_dir+'/page.html')
	expected_output = [line for line in expected_file]
	expected_file.close()
	html_file = open(working_dir+'/html/page.html')
	html_output = [line for line in html_file]
	html_file.close()
	diff = difflib.unified_diff(expected_output, html_output,
		fromfile=working_dir+'/page.html',
		tofile=working_dir+'/html/page.html')
	diff = [line for line in diff]
	os.remove(working_dir+'/html/page.html')
	lib.update_all()
	assert os.path.exists(working_dir+'/html/page.html')
	os.remove(working_dir+'/html/page.html')
	os.rmdir(working_dir+'/html')
	if diff:
		sys.stderr.write(str.join('', diff))
		sys.exit('Web test failed: diff is not empty')

if __name__ == '__main__':
	test_web()
