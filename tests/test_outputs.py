"""End-to-end tests: run the wavescan script and check its output"""

import hashlib
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

from conftest import REPO

WAVESCAN = str(REPO / "wavescan.py")

# what the guesser makes of the sample_dir fixture
GUESSED = {
    "Kick_909.wav": 36,
    "Snare_A.wav": 38,
    "Snare_B.wav": 38,
    "Clap_1.wav": 39,
    "CHH_tight.wav": 42,
    "OHH_long.wav": 46,
    "Laser_zap.wav": 27,
    "floor1.wav": 45,
}
# Mystery_sound.wav is unguessable, Broken_kick.wav is unreadable
SKIPPED = 2


def run(*argv, expect=0):
    proc = subprocess.run(
        [sys.executable, WAVESCAN, *argv],
        capture_output=True, text=True)
    assert proc.returncode == expect, proc.stderr
    return proc


def test_requires_existing_dir(tmp_path):
    proc = run("-d", str(tmp_path / "nope"), expect=1)
    assert "does not exist" in proc.stderr


def test_output_flags_are_mutually_exclusive(sample_dir):
    run("-d", str(sample_dir), "--lsp", "--sfz", expect=2)


def test_channel_validation(sample_dir):
    run("-d", str(sample_dir), "--lsp", "--channel", "17", expect=1)
    run("-d", str(sample_dir), "--lsp", "--channel", "abc", expect=1)


def test_nothing_found(tmp_path):
    proc = run("-d", str(tmp_path), "--sfz")
    assert "nothing found" in proc.stderr
    assert proc.stdout == ""


def test_info_mode(sample_dir):
    proc = run("-d", str(sample_dir))
    # one info block per readable sample, unreadable one warned to stderr
    assert proc.stdout.count("sample rate:") == len(GUESSED) + 1
    assert "skipping unreadable sample" in proc.stderr


def test_unreadable_sample_is_skipped(sample_dir):
    proc = run("-d", str(sample_dir), "--sfz")
    assert "Broken_kick.wav" in proc.stderr
    assert "Broken_kick.wav" not in proc.stdout


def test_sfz(sample_dir):
    proc = run("-d", str(sample_dir), "--sfz", "-D")
    notes = sorted(set(GUESSED.values()))
    groups = [line for line in proc.stdout.splitlines()
              if line.startswith("<group>")]
    assert len(groups) == len(notes)
    for note in notes:
        assert f"key={note} " in proc.stdout
    assert proc.stdout.count("<region>") == len(GUESSED)
    assert f"// unparsed: {SKIPPED}" in proc.stdout
    assert f"// samples: {len(GUESSED)}" in proc.stdout


def test_sfz_multikey(sample_dir):
    proc = run("-d", str(sample_dir), "--sfz", "--sfz-mk")
    assert "pitch_keycenter=36 lokey=36 hikey=36" in proc.stdout


def parse_lsp(stdout):
    kv = {}
    for line in stdout.splitlines():
        if line and not line.startswith("#") and " = " in line:
            k, v = line.split(" = ", 1)
            kv[k] = v
    return kv


def test_lsp(sample_dir):
    proc = run("-d", str(sample_dir), "--lsp", "--channel", "10")
    kv = parse_lsp(proc.stdout)
    sf_keys = [k for k in kv if k.startswith("sf_")]
    assert len(sf_keys) == len(GUESSED)
    # config.ordering puts the kick first
    assert kv["chan_0"] == "9"
    assert kv["note_0"] == "0"   # 36 % 12
    assert kv["oct_0"] == "3"    # 36 // 12
    assert kv["sf_0_0"].endswith('Kick_909.wav"')
    # second snare layer is muted, all first layers enabled
    layer_flags = sorted(v for k, v in kv.items() if k.startswith("on_"))
    assert layer_flags.count("false") == 1
    assert layer_flags.count("true") == len(GUESSED) - 1


def test_lsp_no_mute(sample_dir):
    proc = run("-d", str(sample_dir), "--lsp", "--no-mute")
    kv = parse_lsp(proc.stdout)
    flags = [v for k, v in kv.items() if k.startswith("on_")]
    assert set(flags) == {"true"}


def speedrum_pads(stdout):
    root = ET.fromstring(stdout)
    return root.findall("./Pads/Pad")


def test_speedk(sample_dir):
    proc = run("-d", str(sample_dir), "--speedk")
    pads = speedrum_pads(proc.stdout)
    assert len(pads) == 16
    assert [p.get("PadNum") for p in pads] == [str(n) for n in range(16)]
    for pad in pads:
        assert len(pad.findall("Layer")) <= 1  # Lite is one layered
    names = {p.get("PadName") for p in pads}
    # note 27 is out of Lite range and must be remapped onto a free pad
    assert "High Q / Laser" in names
    proc = run("-d", str(sample_dir), "--speedk", "--no-remap")
    names = {p.get("PadName") for p in speedrum_pads(proc.stdout)}
    assert "High Q / Laser" not in names


def test_speedk_outputs(sample_dir):
    proc = run("-d", str(sample_dir), "--speedk")
    by_name = {p.get("PadName"): p for p in speedrum_pads(proc.stdout)}
    assert by_name["Kick 1"].get("Output") == "0.0"
    assert by_name["Closed HH"].get("Output") == "1.0"
    proc = run("-d", str(sample_dir), "--speedk", "--one-out")
    for pad in speedrum_pads(proc.stdout):
        assert pad.get("Output") is None


def test_speedkit(sample_dir):
    proc = run("-d", str(sample_dir), "--speedkit")
    pads = speedrum_pads(proc.stdout)
    assert len(pads) == 32
    by_name = {p.get("PadName"): p for p in pads if p.get("PadName")}
    snare = by_name["Snare"]
    assert len(snare.findall("Layer")) == 2
    assert snare.get("LayerMode") == "0.0"   # extra layers muted
    assert by_name["Kick 1"].get("LayerMode") == "4.0"
    assert by_name["Kick 1"].get("PadColor")
    # checksum is the md5 of the sample file
    layer = by_name["Kick 1"].find("Layer")
    path = layer.get("SampleFileAbsolute")
    with open(path, "rb") as f:
        assert layer.get("Checksum") == hashlib.md5(f.read()).hexdigest()


def test_speedkit_no_mute(sample_dir):
    proc = run("-d", str(sample_dir), "--speedkit", "--no-mute")
    for pad in speedrum_pads(proc.stdout):
        if pad.get("PadName"):
            assert pad.get("LayerMode") == "4.0"


@pytest.mark.parametrize("flags", [
    [], ["--lsp"], ["--lsp", "--limit"], ["--lsp", "--maxhh", "150"],
    ["--sfz"], ["--sfz", "--sfz-mk"],
    ["--speedk"], ["--speedk", "--one-out"],
    ["--speedkit"], ["--speedkit", "--no-mute"],
])
def test_all_modes_run_clean(sample_dir, flags):
    run("-d", str(sample_dir), "-D", *flags)


def test_wrapper(sample_dir):
    """The wavescan wrapper finds a python3 with the modules on PATH"""
    import os
    env = dict(os.environ)
    env["PATH"] = f"{os.path.dirname(sys.executable)}:{env['PATH']}"
    proc = subprocess.run(
        [str(REPO / "wavescan"), "-d", str(sample_dir), "--sfz"],
        capture_output=True, text=True, env=env)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout.count("<region>") == len(GUESSED)
