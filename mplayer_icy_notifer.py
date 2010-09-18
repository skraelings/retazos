#!/usr/bin/python
from __future__ import print_function
import sys
import errno
import signal
import subprocess


def read_and_notify(mplayerfd):
    current_song = None

    def handler(num, stack):
        if current_song:
            print("You requested current song's title:", current_song,
                  file=sys.stderr)
            args = ['notify-send', "Current song:\n" + current_song]
            subprocess.call(args)
    signal.signal(signal.SIGUSR1, handler)

    while True:
        try:
            line = mplayerfd.readline()
            if "ICY" in line:
                start = line.find("=") + 1
                end = line.find(";")
                current_song = line[start:end]
        except IOError as e:
            if not e.errno == errno.EINTR:
                raise

if __name__ == '__main__':
    read_and_notify(sys.stdin)
