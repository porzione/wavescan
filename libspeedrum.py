#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import hashlib
import audiofile
from libwavescan import warn, WSNote
import config


class Speedrum:

    LITE = 1
    FULL = 2
    ENCODING = "utf-8"
    XML_HEADER = '<?xml version="1.0" encoding="UTF-8"?>'

    def __init__(self, args):
        self.debug = args.debug
        self.no_remap = args.no_remap
        self.one_out = args.one_out
        self.no_mute = args.no_mute
        self.xml_root = ET.Element("Speedrum")
        self.xml_root.set("FileType", "DrumKit")
        self.xml_root.append(ET.Comment('Generated by Wavescan'))
        self.pads = ET.SubElement(self.xml_root, 'Pads')
        if args.speedk:
            self.bound = 52
            self.type = Speedrum.LITE
            self.xml_root.set("version", "2")
            self.xml_root.set("creator", "SpeedrumLite")
        else:
            self.bound = 68
            self.type = Speedrum.FULL
            self.xml_root.set("version", "3")
            self.xml_root.set("creator", "Speedrum")
        self.bank = {}
        self.wsnote = WSNote(args)
        self.c_unparsed = 0

    def size(self):
        return len(self.bank)

    def add(self, ent):
        duration = audiofile.duration(ent.path)
        if (midi_note := self.wsnote.guess(ent, duration)) == 0:
            warn(f"can't guess instrument {ent.path}")
            self.c_unparsed += 1
            return
        if midi_note not in self.bank:
            self.bank[midi_note] = []
        if self.type == Speedrum.LITE and len(self.bank[midi_note]) > 0:
            warn(f"excess Lite layer, skipping {midi_note} {ent.path}")
            return
        if self.type == Speedrum.FULL and len(self.bank[midi_note]) > 7:
            warn(f"already have 8 layers, skipping {midi_note} {ent.path}")
            return
        d = {
            'pathname': ent.path,
            'channels': audiofile.channels(ent.path),
            'duration': duration,
            'samples': audiofile.samples(ent.path),
            'sampling_rate': audiofile.sampling_rate(ent.path),
            'bit_depth': audiofile.bit_depth(ent.path),
        }
        if self.type == Speedrum.FULL:
            d['checksum'] = Speedrum.checksum(ent.path)
        self.bank[midi_note].append(d)

    def checksum(fname):
        """md5 is speedrum's checksum"""
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def fmt_comment(data):
        return f"channels:{data['channels']} " \
            f"duration:{data['duration']} " \
            f"samples:{data['samples']} " \
            f"sampling_rate:{data['sampling_rate']}" \
            f"bit depth:{data['bit_depth']}"

    def remap(self):
        """remap exceess notes to unused pads 36-51/67"""
        free = []
        for k in range(36, self.bound):
            if k not in self.bank:
                free.append(k)
        if len(free) == 0:
            return {}
        excess = []
        for k, v in self.bank.items():
            if k >= self.bound or k < 36:
                excess.append(k)
        if len(excess) == 0:
            return {}
        sr_map = {}
        for e in excess:
            if len(free) > 0:
                f = free.pop(0)
                sr_map[e] = f
        return sr_map

    def build(self):
        if self.type == Speedrum.LITE:
            self.build_speedk()
        elif self.type == Speedrum.FULL:
            self.build_speedkit()

    def build_speedk(self):
        pads = {k: [] for k in range(36, 52)}
        remap = {} if self.no_remap else self.remap()
        for note, layers in sorted(self.bank.items()):
            r_note = note
            if note in remap:
                r_note = remap[note]
                if self.debug:
                    warn(f"remap: {note} -> {r_note}")
            d = {
                'name': config.names[note],
                'layers': layers,
            }
            # 16 (36-51) pads in Lite
            if not self.one_out:
                if note in config.ordering:
                    d['out'] = config.ordering.index(note)
                else:
                    d['out'] = 0
            if 35 <= r_note <= 51:
                pads[r_note] = d
            elif self.debug:
                warn(f"out of Speedrum Lite range: {note} / {layers}")

        pad_num = 0
        for num, data in pads.items():
            pad = ET.SubElement(self.pads, 'Pad')
            pad.set("PadNum", str(pad_num))
            pad_num += 1
            if len(data) == 0:
                continue
            pad.set("PadName", data['name'])
            pad.set("IsCustomName", "1")
            if 'out' in data:
                pad.set("Output", f"{data['out']}.0")
            for ld in data['layers']:
                layer = ET.SubElement(pad, 'Layer')
                layer.set("SampleFileAbsolute", ld["pathname"])
                # Lite is one layered
                layer.set("LayerNum", "0")
                if self.debug:
                    comment = Speedrum.fmt_comment(ld)
                    layer.append(ET.Comment(comment))

        print(Speedrum.XML_HEADER)
        ET.indent(self.xml_root, space="\t", level=0)
        print(ET.tostring(
            self.xml_root, Speedrum.ENCODING)
            .decode(Speedrum.ENCODING))

    def build_speedkit(self):
        pads = {k: [] for k in range(36, 68)}
        remap = {} if self.no_remap else self.remap()
        for note, layers in sorted(self.bank.items()):
            r_note = note
            if note in remap:
                r_note = remap[note]
                if self.debug:
                    warn(f"remap: {note} -> {r_note}")
            d = {
                'name': config.names[note],
                'layers': layers,
            }
            # 32 (36-67) in full version
            if not self.one_out:
                if note in config.ordering:
                    d['out'] = config.ordering.index(note)
                else:
                    d['out'] = 0
            if 36 <= r_note <= 67:
                pads[r_note] = d
            elif self.debug:
                warn(f"out of Speedrum range: {note} / {layers}")

        for num, data in pads.items():
            pad = ET.SubElement(self.pads, 'Pad')
            if len(data) == 0:
                continue
            pad.set("PadName", data['name'])
            pad.set("IsCustomName", "1")
            pad.set("LayerIndex", "0")
            if 'out' in data:
                pad.set("Output", f"{data['out']}.0")
            lc = 0
            for ld in data['layers']:
                layer = ET.SubElement(pad, 'Layer')
                layer.set("SampleFileAbsolute", ld["pathname"])
                layer.set("Checksum", ld['checksum'])
                if lc > 0 and not self.no_mute:
                    layer.set("Volume", "0.0")
                if self.debug:
                    comment = Speedrum.fmt_comment(ld)
                    layer.append(ET.Comment(comment))
                lc += 1

        print(Speedrum.XML_HEADER)
        ET.indent(self.xml_root, space="\t", level=0)
        print(ET.tostring(
            self.xml_root, Speedrum.ENCODING
            ).decode(Speedrum.ENCODING))