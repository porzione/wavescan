#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import dirname, realpath
from jinja2 import Template as J2, StrictUndefined as J2Undef
from libwavescan import warn, probe, WSNote
import config


class LSP:

    def __init__(self, args, midi_channel):
        self.debug = args.debug
        self.midi_channel = midi_channel
        self.limit = args.limit
        self.no_mute = args.no_mute
        s_path = dirname(realpath(__file__))
        with open(f'{s_path}/lsp-sampler.j2', 'r', encoding='ascii') as fin:
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
            warn(f"can't guess: {ent.path}")
            self.c_unparsed += 1
            return

        entry = self.bank.get(midi_note)
        if self.limit:
            if entry and len(entry['l']) >= config.MAX_SAMPLES:
                warn(f"samples limit: {midi_note} {ent.path}")
                return
            if entry is None and self.size() >= config.MAX_INSTRUMENTS:
                warn(f"instruments limit: {midi_note} {ent.path}")
                return

        if entry is None:
            entry = self.bank[midi_note] = {
                'i': {
                    'lsp_note': midi_note % 12,
                    'midi_note': midi_note,
                    'midi_name': config.names[midi_note],
                    'oct': int(midi_note / 12),
                },
                'l': []
            }
        is_enabled = 'true'
        if len(entry['l']) > 0 and not self.no_mute:
            is_enabled = 'false'
        entry['l'].append({
            'pathname': ent.path,
            'is_enabled': is_enabled,
            # workaround for mono
            'pan_l': '0.0' if info['channels'] == 1 else '-100.0',
            **info,
        })

    @staticmethod
    def order(key):
        if key[0] in config.ordering:
            return config.ordering.index(key[0])
        else:
            return key[0] + 1000

    def build(self):
        print(self.tpl.render({
            'notes': sorted(self.bank.items(), key=LSP.order),
            'midi_channel': self.midi_channel,
            'debug': self.debug,
        }))
