import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(REPO))

import pytest  # noqa: E402


class FakeEnt:
    """Stands in for an os.DirEntry"""

    def __init__(self, path):
        self.path = path
        self.name = path.rsplit("/", 1)[-1]


class FakeArgs:
    """Stands in for parsed CLI arguments"""

    debug = False
    maxhh = None
    limit = False
    no_mute = False


@pytest.fixture
def fake_args():
    return FakeArgs()


@pytest.fixture(scope="session")
def corpus_paths():
    """Real drum library paths harvested from an ls -lR listing"""
    text = (FIXTURES / "drum_paths.txt").read_text(encoding="utf-8")
    return text.splitlines()


@pytest.fixture(scope="session")
def corpus_golden():
    """Expected guess() result for every corpus path: {path: note}"""
    golden = {}
    text = (FIXTURES / "guess_golden.txt").read_text(encoding="utf-8")
    for line in text.splitlines():
        note, path = line.split("\t", 1)
        golden[path] = int(note)
    return golden


@pytest.fixture(scope="session")
def sample_dir(tmp_path_factory):
    """Small on-disk sample library with known content"""
    import numpy as np
    import audiofile

    root = tmp_path_factory.mktemp("samples")
    (root / "TOMS").mkdir()
    sr = 44100
    for name, seconds in [
        ("Kick_909.wav", 0.30),
        ("Snare_A.wav", 0.20),
        ("Snare_B.wav", 0.20),
        ("Clap_1.wav", 0.15),
        ("CHH_tight.wav", 0.05),
        ("OHH_long.wav", 0.60),
        ("Laser_zap.wav", 0.10),
        ("Mystery_sound.wav", 0.10),
        ("TOMS/floor1.wav", 0.25),
    ]:
        sig = np.zeros(int(sr * seconds), dtype="float32")
        sig[0] = 0.5
        audiofile.write(str(root / name), sig, sr)
    (root / "Broken_kick.wav").write_bytes(b"not really a wav file")
    return root
