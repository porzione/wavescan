"""Tests for WSNote.guess() — the file-name-to-drum heuristic"""

import pytest

from libwavescan import WSNote
from conftest import FakeArgs, FakeEnt


@pytest.fixture(scope="module")
def wsnote():
    return WSNote(FakeArgs())


# hand-picked cases, including regressions for fixed config bugs
KNOWN = [
    ("Kick_909.wav", 36),
    ("kik_hard.flac", 36),
    ("TR808_BassDrum_04.wav", 36),
    ("Acoustic Bass Drum 1.wav", 35),
    ("Snare_Tight.wav", 38),
    ("SD_Snare_Transistor.flac", 38),      # README example
    ("ESnare_04.wav", 40),
    ("Clap_Big.wav", 39),
    ("SD_ClHat_Gentle.flac", 42),          # README example
    ("HH_cl_soft.wav", 42),                # regression: corrupted regex
    ("CHH_1.wav", 42),
    ("OHH_1.wav", 46),
    ("Hat_Open_3.wav", 46),
    ("Pedal_HiHat_2.wav", 44),
    ("Low_Tom_A.wav", 45),
    ("Crash_18.wav", 49),
    ("Ride_20.wav", 51),
    ("Splash_10.wav", 55),
    ("Cowbell_808.wav", 56),
    ("Low_Bongo_1.wav", 61),               # regression: was shadowed by "bongo"
    ("Bongo_1.wav", 60),
    ("Mute_Conga.wav", 62),
    ("Open_Conga.wav", 63),
    ("Hi_Conga_1.wav", 63),                # regression: was 62 Mute Hi Conga
    ("Conga_Solo.wav", 64),
    ("Maracas_1.wav", 70),
    ("Shaker_Soft.wav", 82),
    ("Laser_zap.wav", 27),
    ("Mystery_sound.wav", 0),
    # directory names take part in guessing
    ("KICKS/tight1.wav", 36),
    ("TOMS/floor1.wav", 45),
    ("HI HATS/x1.wav", 42),
]


@pytest.mark.parametrize("path,expected", KNOWN,
                         ids=[k[0] for k in KNOWN])
def test_known_names(wsnote, path, expected):
    assert wsnote.guess(FakeEnt(path), 0) == expected


def test_maxhh_splits_unknown_hats():
    args = FakeArgs()
    args.maxhh = "150"
    ws = WSNote(args)
    # "SomeHat" only matches the generic "hat" rule (note 1000)
    assert ws.guess(FakeEnt("SomeHat_1.wav"), 0.1) == 42
    assert ws.guess(FakeEnt("SomeHat_1.wav"), 0.2) == 46


def test_unknown_hat_defaults_to_closed(wsnote):
    assert wsnote.guess(FakeEnt("SomeHat_1.wav"), 99.0) == 42


@pytest.mark.parametrize("bad", ["abc", "0", "1000"])
def test_maxhh_validation(bad):
    args = FakeArgs()
    args.maxhh = bad
    with pytest.raises(SystemExit):
        WSNote(args)


def test_corpus_against_golden(corpus_paths, corpus_golden, wsnote):
    """Every path of the real drum library must keep guessing the same.

    On intentional guesser changes regenerate the golden file:
        python tests/regen_golden.py
    """
    mismatches = []
    for path in corpus_paths:
        got = wsnote.guess(FakeEnt(path), 0)
        want = corpus_golden[path]
        if got != want:
            mismatches.append(f"{path}: expected {want}, got {got}")
    assert not mismatches, (
        f"{len(mismatches)} corpus guesses changed, first 20:\n"
        + "\n".join(mismatches[:20])
    )


def test_corpus_coverage(corpus_paths, wsnote):
    """Overall hit rate on the real library must not regress"""
    guessed = sum(
        1 for p in corpus_paths if wsnote.guess(FakeEnt(p), 0) != 0
    )
    assert guessed / len(corpus_paths) >= 0.86
