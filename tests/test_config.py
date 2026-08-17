"""Sanity checks for config.py"""

import re

import config
from libwavescan import WSNote
from conftest import FakeArgs


def test_all_instrument_regexes_compile():
    ws = WSNote(FakeArgs())
    # WSNote warns and drops broken regexes; none may be dropped
    assert len(ws.rx_instr) == len(config.instruments)


def test_instrument_notes_have_names():
    for rx, note in config.instruments:
        if note == 1000:  # "some hihat" sentinel
            continue
        assert note in config.names, f"no name for note {note} ({rx})"


def test_ordering_is_16_unique_named_notes():
    assert len(config.ordering) == 16
    assert len(set(config.ordering)) == 16
    for note in config.ordering:
        assert note in config.names


def test_colors_reference_named_notes():
    for note, color in config.colors.items():
        assert note in config.names
        assert re.fullmatch(r"[0-9a-f]{8}", color)


def test_scan_regexes():
    sample = re.compile(config.SAMPLE, re.I)
    assert sample.match("x.wav")
    assert sample.match("x.FLAC")
    assert sample.match("x.aif")
    assert sample.match("x.aiff")
    assert sample.match("x.aifc")
    assert not sample.match("x.wav.asd")
    assert not sample.match("x.mp3")
    ignore = re.compile(config.IGNORE, re.I)
    assert ignore.match("/audio/synth wavetable/x.wav")
    assert not ignore.match("/audio/drums/x.wav")


def test_lsp_limits():
    assert config.MAX_INSTRUMENTS == 48
    assert config.MAX_SAMPLES == 8
