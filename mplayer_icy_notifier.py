#!/usr/bin/python
# Author: Reynaldo Baquerizo <reynaldomic@gmail.com>
# Date: August 2010
from __future__ import print_function
import sys
import errno
import signal
import subprocess


def read_and_notify(mplayerfd, output=None):
    current_song = None

    def handler(num, stack):
        if current_song:
            print("You requested current song's title:", current_song,
                  file=sys.stderr)
            if output:
                output.writelines(current_song + '\n')
                output.flush()
            args = ["notify-send", "Current song:\n" + current_song]
            subprocess.call(args)
    # Register the handler
    signal.signal(signal.SIGUSR1, handler)

    while True:
        try:
            line = mplayerfd.readline()
            if "ICY" in line:
                start = line.find("=") + 1
                end = line.find(";")
                current_song = line[start:end]
        except IOError as detail:
            if not detail.errno == errno.EINTR:
                raise
        except KeyboardInterrupt:
            output.close()
            break

if __name__ == "__main__":
    output = open('.favorites.song')
    read_and_notify(sys.stdin, output)
