#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import stderr
import re
import audiofile
import config


def warn(msg):
    """print message to stderr"""
    print(msg, file=stderr)


def print_info(ent):
    """Print sample info"""
    print(f'{ent.path}\n'
          f'channels   : {audiofile.channels(ent.path)}\n'
          f'duration   : {audiofile.duration(ent.path):.8}\n'
          f'samples    : {audiofile.samples(ent.path)}\n'
          f'sample rate: {audiofile.sampling_rate(ent.path)}\n'
          f'bit depth  : {audiofile.bit_depth(ent.path)}\n')


class WSNote:

    def __init__(self, args):
        self.debug = args.debug
        self.maxhh = 0
        if args.maxhh:
            if not args.maxhh.isnumeric():
                exit(f"HH duration '{args.maxhh}' not a number")
            self.maxhh = int(args.maxhh)
            if not 1 <= self.maxhh <= 999:
                exit(f"HH duration '{self.maxhh}' is out of range")
            self.maxhh /= 1000
        # array of arrays [compiled_regex, note_number]
        self.rx_instr = []
        for rx in config.instruments:
            try:
                self.rx_instr.append([
                    re.compile(f".*{rx[0]}.+", re.I),
                    rx[1]
                ])
            except re.error as err:
                warn(f"problem with regex '{rx[0]}': {err}")

    def guess(self, ent, duration):
        """Tryng to guess instrument from pathname"""
        for rx in self.rx_instr:
            if rx[0].match(ent.path):
                num = rx[1]
                dur_msg = None
                if num == 1000:
                    # closed: 42, open: 46
                    if self.maxhh:
                        (num := 46) if duration > self.maxhh else (num := 42)
                        dur_msg = f"duration: {duration}, maxhh: {self.maxhh}"
                    else:
                        # Answer to the Ultimate Question
                        num = 42
                if self.debug:
                    human_name = f"{rx[0].pattern} {num} {config.names[num]}"
                    msg = f"guess {ent.name} is {human_name}"
                    if dur_msg:
                        msg = f"{msg} ({dur_msg})"
                    warn(msg)
                return num
        return 0
