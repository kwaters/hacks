#!/usr/bin/env python3

import argparse
import pickle
import re
import zlib
import os


def unrpa(archive):
    header_re = re.compile(
        br'^RPA-3\.0\s+([0-9a-fA-F]+)\s+([0-9a-fA-F]+)\s+$')

    firstline = archive.readline()
    match = header_re.match(firstline)
    assert match, "Invalid file."

    offset = int(match.group(1), 16)
    key = int(match.group(2), 16)

    archive.seek(0)
    raw = archive.read()
    archive.close()

    files = pickle.loads(zlib.decompress(raw[offset:]))

    for fpath, ((foffset, fsize, *_),) in files.items():
        foffset = foffset ^ key
        fsize = fsize ^ key

        print(fpath)
        dirname = os.path.dirname(fpath)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        with open(fpath, 'wb') as f:
            f.write(raw[foffset:foffset + fsize])


def main():
    args = argparse.ArgumentParser()
    args.add_argument('RPA', nargs='+', type=argparse.FileType('rb'))
    opts = args.parse_args()

    for rpa in opts.RPA:
        unrpa(rpa)


if __name__ == '__main__':
    main()
