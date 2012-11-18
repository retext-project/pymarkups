import sys
import unittest

if sys.version_info[0] < 3 and 'setup.py' not in sys.argv[0]:
	from test_public_api import APITest
	from test_markdown import MarkdownTest
	from test_restructuredtext import ReStructuredTextTest
	from test_web import WebTest

def main():
	if sys.version_info[0] >= 3:
		from unittest.main import main
		main(module=None)
	else:
		unittest.main()

if __name__ == '__main__':
	main()
