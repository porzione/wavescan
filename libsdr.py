#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib


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


def remap(speedrum, bound):
    """remap exceess notes to unused pads 36-51/67"""
    free = []
    for k in range(36, bound):
        if k not in speedrum:
            free.append(k)
    if len(free) == 0:
        return {}
    excess = []
    for k, v in speedrum.items():
        if k >= bound or k < 36:
            excess.append(k)
    if len(excess) == 0:
        return {}
    sr_map = {}
    for e in excess:
        if len(free) > 0:
            f = free.pop(0)
            sr_map[e] = f
    return sr_map
