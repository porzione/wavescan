# Generate drum kits from audio files

The script tries to guess the drum type from its file name, e.g. `SD_ClHat_Gentle.flac` is a Closed Hi-Hat (MIDI note 42), `SD_Snare_Transistor.flac` is a Snare (MIDI note 38) and so on. Regular expressions are in `config.py`.

wavescan recursively goes through wav/flac/aif samples in the directory given with `-d` and prints a text config for importing into

- [LSP sampler](https://lsp-plug.in/) (`--lsp`)

- [Speedrum](https://www.apisoniclabs.com/) Lite (`--speedk`) and full version (`--speedkit`)

- [SFZ](https://sfzformat.com/) enabled software (`--sfz`), tested with [sfizz](https://sfz.tools/sfizz/) and [Redux](https://www.renoise.com/products/redux/)

Without an output option it just prints info about the found samples.

Speedrum Lite is limited to 16 pads with MIDI notes 36-51 (32 pads, notes 36-67 in the full version); notes outside that range are remapped to free pads unless `--no-remap` is given. Debug messages and warnings are printed to stderr, the generated config goes to stdout.

## requirements

Python 3.9+ with a couple of modules:

```bash
pip install -r requirements.txt
```

## tests

```bash
pip install -r requirements-dev.txt
pytest
```

The guesser is regression-tested against `tests/fixtures/drum_paths.txt` — 4509 file paths from a real drum sample library — with the expected guess for each recorded in `tests/fixtures/guess_golden.txt`. After an intentional change to the rules in `config.py`, regenerate the golden file with `python tests/regen_golden.py` and review the diff.

## examples

scan directory tree for samples, store LSP config in 'dk909.cfg'

`wavescan -d /audio/H2/Roland_TB909Kit/ --lsp > dk909.cfg`

print debug messages and add comments to config (`-D`), also respect LSP limits (`--limit`) with max 48 instruments and 8 samples per each

`wavescan -d /audio/Drums/KITS/KIT_TECH/ --lsp -D --limit > SFZ_TECH.cfg`

use MIDI channel 10 instead of default 1

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --channel 10`

if it's an unknown hi-hat, use 150ms duration to decide if it's open or closed

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --maxhh 150`

print SFZ soundfont

`wavescan -d /audio/Drums/my/ --sfz > ~/Music/SFZ/my.sfz`

the same but with extended midi key syntax (lokey/hikey/pitch_keycenter instead of just key)

`wavescan -d /audio/Drums/my/ --sfz --sfz-mk > ~/Music/SFZ/my.sfz`

make Speedrum Lite kit

`wavescan -d /audio/Drums/my/ --speedk -D > ~/Music/Speedrum/my.speedk`

make Speedrum kit

`wavescan -d /audio/Drums/my/ --speedkit -D > ~/Music/Speedrum/my.speedkit`

one direct out for all drums (separate outs by default)

`wavescan -d /audio/Drums/my/ --speedk --one-out`

do not mute/disable additional layers, by default only the first one is enabled

`wavescan -d /audio/Drums/my/ --speedkit --no-mute`
