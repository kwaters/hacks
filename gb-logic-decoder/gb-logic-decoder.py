#!/usr/bin/env python
# Copyright (C) 2011 by Kenneth Waters
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import numpy
import PIL.Image


def load_trace(fp):
    header = fp.readline().split()
    raw = [[int(s) for s in line.split()] for line in fp]
    return numpy.array(raw, dtype=numpy.uint8)


def triggered_rows(a):
    tsignals = a[:, [3, 0, 4]]

    # pixel clock is neg-edge triggered
    tsignals[:, 0] = 1 - tsignals[:, 0]

    triggers = numpy.logical_and(numpy.logical_not(tsignals[:-1]), tsignals[1:])
    rows = numpy.logical_or.reduce(triggers, axis=1)
    signals = a[1:][rows][:, [1, 2]]
    return numpy.append(signals, triggers[rows], axis=1)


def frame(data):
    pixel_rows = data[data[:, 2] != 0]
    pixels = numpy.sum(pixel_rows[:, 0:2] * [1, 2], axis = 1, dtype=numpy.uint8)

    # Move to [0, 255] range
    pixels = 255 - 85 * pixels

    # assume every row has the same number of pixels
    row_count = data.sum(axis=0)[3]
    pixels = pixels.reshape((row_count, len(pixels) // row_count))

    image = PIL.Image.fromarray(pixels)
    return image


def main():
    trace = load_trace(file('logic-capture-actually-a-txt-file.doc', 'U'))
    data = triggered_rows(trace)
    image = frame(data)
    image.save("frame.png")


if __name__ == '__main__':
    main()
