#!/usr/bin/env python

"""Unpack the images from Race for the Galaxy.

http://www.keldon.net/rftg/

"""

import struct
import sys

class Field(object):
    def __init__(self, fmt, name_fmt):
        self.s = struct.Struct(fmt)
        self.size = self.s.size
        self.name_fmt = name_fmt

    def decode(self, raw, pos):
        c, name, size = self.s.unpack_from(raw, pos)
        name = self.name_fmt.format(c=ord(c), name=name.rstrip('\0'))
        size = int(size.rstrip('\0'))
        return name, size


def main():
    raw = open(sys.argv[1]).read()

    assert raw[:4] == 'RFTG'
    pos = 4

    headers = {
        '\x01': Field('c4s8s', 'card{name}.jpg'),
        '\x02': Field('c0s8s', 'card-back.jpg'),
        '\x03': Field('c3s8s', 'goal-{name}.jpg'),
        '\x04': Field('c3s8s', 'icon-{name}.png'),
        '\x05': Field('c3s8s', 'action-{name}.jpg'),
    }

    while raw[pos] != '\0':
        field = headers[raw[pos]]
        name, size = field.decode(raw, pos)
        pos += field.size

        with file(name, 'wb') as outfile:
            outfile.write(raw[pos:pos + size])

        pos += size

if __name__ == '__main__':
    main()
