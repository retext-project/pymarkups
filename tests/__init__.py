import sys
import unittest

def main():
	if sys.version_info[0] >= 3:
		from unittest.main import main
		main(module=None)
	else:
		unittest.main()

if __name__ == '__main__':
	main()
