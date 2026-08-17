#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, realpath
from jinja2 import Template as J2, StrictUndefined as J2Undef
from libwavescan import warn, probe, WSNote
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

    def size(self):
        return len(self.bank)

    def add(self, ent):
        if (info := probe(ent.path)) is None:
            self.c_unparsed += 1
            return
        if (midi_note := self.wsnote.guess(ent, info['duration'])) == 0:
            warn(f"can't guess instrument: {ent.path}")
            self.c_unparsed += 1
            return
        self.bank.setdefault(midi_note, []).append({
            'pathname': ent.path,
            **info,
        })

    def build(self):
        regions = [{
            'midi_note': midi_note,
            'midi_name': config.names[midi_note],
            'samples': samples
        } for midi_note, samples in sorted(self.bank.items())]

        print(self.tpl.render({
            'multikey': self.multikey,
            'regions': regions,
            'debug': self.debug
        }))

        if self.debug:
            print(f"// unparsed: {self.c_unparsed}\n"
                  f"// regions: {len(self.bank)}\n"
                  f"// samples: {sum(map(len, self.bank.values()))}"
                  )
