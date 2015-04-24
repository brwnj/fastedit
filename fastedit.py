#!/usr/bin/env python
# coding=utf-8

from __future__ import print_function

import argparse
import gzip
import os
import sys
from csv import reader
from itertools import groupby

gzopen = lambda f: gzip.open(f) if f.endswith(".gz") else open(f)


def readfa(fa):
    with gzopen(fa) as fh:
        for header, group in groupby(fh, lambda line: line[0] == '>'):
            if header:
                line = group.next()
                name = line[1:].strip()
            else:
                seq = ''.join(line.strip() for line in group)
                yield name, seq


def get_headers(fasta, out, verbose=False):
    total = 0
    with open(out, 'w') if out else sys.stdout as fh:
        for name, seq in readfa(fasta):
            total += 1
            print(name, file=fh)
    if verbose:
        print(total, "headers exported.", file=sys.stderr)


def put_headers(fasta, csv, out, verbose=False):
    headers = {}
    with open(csv, 'rU') as fh:
        it = reader(fh)
        for r in it:
            try:
                headers[r[0]] = r[1].lstrip(">")
            except IndexError:
                headers[r[0]] = ''

    total = 0
    renamed = 0
    ignored = 0
    with open(out, 'w') if out else sys.stdout as fh:
        for name, seq in readfa(fasta):
            total += 1
            try:
                newname = headers[name]
                if newname:
                    renamed += 1
                else:
                    # in the csv, but no new name
                    newname = name

                # print the record
                print(">%s" % newname, file=fh)
                for i in xrange(0, len(seq), 60):
                    print(seq[i:i + 60], file=fh)

            except KeyError:
                # removed from the csv
                ignored += 1

    if verbose:
        print("Input fasta contained", total, "records", file=sys.stderr)
        print("You renamed", renamed, "and kept a total of", total - ignored,
              file=sys.stderr)


def file_exists(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist." % arg)
    return arg


def main():
    parser = argparse.ArgumentParser(version="0.1.4")
    subparsers = parser.add_subparsers()

    get_parser = subparsers.add_parser(
        'get',
        description=("Pull out the headers from <fasta> and write them "
                     "to <out>."),
        help="step 1 - retrieve the headers from the fasta")
    get_parser.add_argument("fasta",
                            type=lambda x: file_exists(parser, x),
                            help="fasta file")
    get_parser.add_argument("-o", "--out", help="output file")
    get_parser.add_argument("--verbose",
                            action="store_true",
                            help="print record count after processing")
    get_parser.set_defaults(func=get_headers)

    put_parser = subparsers.add_parser(
        'put',
        description=("Replace <fasta> headers with column 2 of <csv> where "
                     "column 1 matches the original header in <fasta>. "
                     "Headers will only be altered for <csv> entries with 2 "
                     "columns. Rows removed from <csv> will be removed "
                     "from the output."),
        help="step 2 - replace the headers using your csv")
    put_parser.add_argument("fasta",
                            type=lambda x: file_exists(parser, x),
                            help="fasta file")
    put_parser.add_argument("csv",
                            type=lambda x: file_exists(parser, x),
                            help="csv with old and new headers")
    put_parser.add_argument("-o", "--out", help="output file")
    put_parser.add_argument("--verbose",
                            action="store_true",
                            help="print renaming metrics after processing")
    put_parser.set_defaults(func=put_headers)

    args = vars(parser.parse_args())
    func = args.pop("func")
    func(**args)


if __name__ == '__main__':
    main()
