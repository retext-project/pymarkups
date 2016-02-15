#!/usr/bin/env python3

import argparse
import markups
import sys


def export_file(args):
    markup = markups.get_markup_for_file_name(args.input_file)
    with open(args.input_file) as input:
        text = input.read()
    if not markup:
        sys.exit('Markup not available.')
    converted = markup.convert(text)

    html = converted.get_whole_html(include_stylesheet=args.include_stylesheet,
                                    fallback_title=args.fallback_title,
                                    webenv=args.web_environment)

    with open(args.output_file, 'w') as output:
        output.write(html)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--web-environment', help='export for web environment',
                        action='store_true')
    parser.add_argument('--include-stylesheet', help='embed the stylesheet into html',
                        action='store_true')
    parser.add_argument('--fallback-title', help='fallback title of the HTML document',
                        metavar='TITLE')
    parser.add_argument('input_file', help='input file')
    parser.add_argument('output_file', help='output file')
    args = parser.parse_args()
    export_file(args)
