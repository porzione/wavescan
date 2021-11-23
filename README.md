# Generate drum kits from audio files

Script tries to guess drum type from its file name e.g. `SD_ClHat_Gentle.flac` is Closed Hi Hat (MIDI note 42), `SD_Snare_Transistor.flac` is Snare (MIDI note 38) and so on. Regular expressions are in `config.py`.

wavescan recursively goes through  wav/flac/aif samples in provided with `-d` directory and prints text config for importing into

- [LSP sampler](https://lsp-plug.in/)

- [Speedrum drum samples](https://www.apisoniclabs.com/)

- [SFZ](https://sfzformat.com/)  enabled software, tested with [sfizz](https://sfz.tools/sfizz/) and [Redux](https://www.renoise.com/products/redux).

Speedrum Lite is limited by 16 MIDI notes with numbers 36-51 (36-67 in full version). Debug messages are printing to stderr.

## requirements

python 3.9 with couple of modules

```bash
pip install audiofile
pip install Jinja2
```

## examples

scan directory tree for samples, store LSP config in 'dk900.cfg'

`wavescan -d /audio/H2/Roland_TB909Kit/ --lsp > dk909.cfg`

print debug messages and add comments to config  (`-D`), also respect LSP limits (`--limit`) with max 48 instruments and 8 samples per each

`wavescan -d /audio/Drums/KITS/KIT_TECH/ --lsp -D --limit > SFZ_TECH.cfg`

use MIDI channel 10 instead of default 1

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --channel 10`

if it's unknown hi-hat, use 150ms duration to decide if it's open or closed

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --maxhh 150`

print SFZ soundfont

`wavescan -d /audio/Drums/my/ --sfz > ~/Music/SFZ/my.sfz`

the same but with extended midi key syntax

`wavescan -d /audio/Drums/my/ --sfz --sfz-mk > ~/Music/SFZ/my.sfz`

make Speedrum Lite bank

`wavescan -d /audio/Drums/my/ --speedk -D > ~/Music/Speedrum/my.speedk`

make Speedrum bank

`wavescan -d /audio/Drums/my/ --speedkit -D > ~/Music/Speedrum/my.speedkit`

one direct out for all drums (separate outs by default)

`wavescan -d /home/ftp/audio/Drums/my/ --speedk --one-out`
