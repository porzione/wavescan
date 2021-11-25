#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, realpath
from jinja2 import Template as J2, StrictUndefined as J2Undef
import audiofile
from libwavescan import warn, WSNote
import config


class SFZ:

    def __init__(self, args):
        self.debug = args.debug
        self.multikey = args.sfz_mk
        s_path = dirname(realpath(__file__))
        with open(f'{s_path}/sfz.j2', 'r', encoding='ascii') as fin:
            src = fin.read()
        self.tpl = J2(src, undefined=J2Undef)
        self.bank = {}
        self.wsnote = WSNote(args)
        self.c_unparsed = 0
        self.c_samples = 0

    def size(self):
        return len(self.bank)

    def add(self, ent):
        duration = audiofile.duration(ent.path)
        if (midi_note := self.wsnote.guess(ent, duration)) == 0:
            warn(f"can't guess instrument: {ent.path}")
            self.c_unparsed += 1
            return
        if midi_note not in self.bank:
            self.bank[midi_note] = []
        self.bank[midi_note].append({
            'pathname': ent.path,
            'channels': audiofile.channels(ent.path),
            'duration': duration,
            'samples': audiofile.samples(ent.path),
            'sampling_rate': audiofile.sampling_rate(ent.path),
            'bit_depth': audiofile.bit_depth(ent.path),
        })

    def build(self):
        regions = []
        c_samples = 0

        for reg_key, samples in sorted(self.bank.items()):
            regions.append({
                'midi_note': reg_key,
                'midi_name': config.names[reg_key],
                'samples': samples
            })

            c_samples += len(samples)

        print(self.tpl.render({
            'multikey': self.multikey,
            'regions': regions,
            'debug': self.debug
        }))

        if self.debug:
            print(f"// unparsed: {self.c_unparsed}\n"
                  f"// regions: {len(self.bank)}\n"
                  f"// samples: {self.c_samples}"
                  )
