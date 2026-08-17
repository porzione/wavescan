# Generate drum kits from audio files

wavescan builds a drum kit from a directory of assorted samples, guessing each sample's drum type from its file name: `SD_ClHat_Gentle.flac` is a Closed Hi-Hat (MIDI note 42), `SD_Snare_Transistor.flac` is a Snare (MIDI note 38) and so on. The regular expressions doing the guessing are in `config.py`.

It recursively scans the directory given with `-d` for wav/flac/aiff samples and prints a text config for importing into

- [LSP sampler](https://lsp-plug.in/) (`--lsp`)

- [Speedrum](https://www.apisoniclabs.com/) Lite (`--speedk`) and full version (`--speedkit`)

- [SFZ](https://sfzformat.com/)-enabled software (`--sfz`), tested with [sfizz](https://sfz.tools/sfizz/) and [Redux](https://www.renoise.com/products/redux/)

Without an output option it just prints info about each sample it finds.

Speedrum Lite is limited to 16 pads with MIDI notes 36-51 (the full version: 32 pads, notes 36-67); notes outside that range are remapped to free pads unless `--no-remap` is given. The generated config goes to stdout; debug messages and warnings go to stderr.

## requirements

Python 3.9+ and two modules, `audiofile` and `Jinja2`. The `wavescan` wrapper runs `wavescan.py` with the system Python if the modules are importable; otherwise it falls back to [uv](https://docs.astral.sh/uv/), which creates a cached environment with the modules automatically. So either install them:

```bash
pip install -r requirements.txt
```

or just have uv installed and forget about it.

## tests

```bash
pip install -r requirements-dev.txt
pytest
```

The guesser is regression-tested against `tests/fixtures/drum_paths.txt` — 4509 file paths from a real drum sample library — with the expected guess for each recorded in `tests/fixtures/guess_golden.txt`. After an intentional change to the rules in `config.py`, regenerate the golden file with `python tests/regen_golden.py` and review the diff.

## examples

scan a directory tree for samples, store the LSP config in `dk909.cfg`

`wavescan -d /audio/H2/Roland_TB909Kit/ --lsp > dk909.cfg`

print debug messages and add comments to the config (`-D`), also respect LSP limits (`--limit`): max 48 instruments with 8 samples each

`wavescan -d /audio/Drums/KITS/KIT_TECH/ --lsp -D --limit > SFZ_TECH.cfg`

use MIDI channel 10 instead of the default 1

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --channel 10`

for hi-hats of unknown type, treat samples longer than 150 ms as open, shorter as closed

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --maxhh 150`

print SFZ soundfont

`wavescan -d /audio/Drums/my/ --sfz > ~/Music/SFZ/my.sfz`

the same but with extended MIDI key syntax (lokey/hikey/pitch_keycenter instead of just key)

`wavescan -d /audio/Drums/my/ --sfz --sfz-mk > ~/Music/SFZ/my.sfz`

make Speedrum Lite kit

`wavescan -d /audio/Drums/my/ --speedk -D > ~/Music/Speedrum/my.speedk`

make Speedrum kit

`wavescan -d /audio/Drums/my/ --speedkit -D > ~/Music/Speedrum/my.speedkit`

one direct out for all drums (separate outs by default)

`wavescan -d /audio/Drums/my/ --speedk --one-out`

do not mute additional layers (by default only the first layer of each drum is enabled)

`wavescan -d /audio/Drums/my/ --speedkit --no-mute`
