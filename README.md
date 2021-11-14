# Generate drum kit for LSP sampler or SFZ from audio files

Find wav/flac/aif samples in provided with `-d` directory and print text config for importing into [LSP](https://lsp-plug.in/) sampler. SFZ output contains only key and sample opcodes, tested with [sfizz](https://sfz.tools/sfizz/). Debug messages are printing to stderr.

## requirements

python 3.9 with couple of modules

```bash
pip install audiofile
pip install Jinja2
```

## examples

scan directory tree for samples, store config in 'dk900.cfg'

`wavescan -d /audio/H2/Roland_TB909Kit --lsp > dk909.cfg`

print debug messages and add comments to config  (`-D`), also respect LSP limits (`--limit`) with max 48 instruments and 8 samples per each

`wavescan -d /audio/Drums/KITS/KIT_TECH/ --lsp -D --limit > SFZ_TECH.cfg`

use MIDI channel 10 instead of default 1

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --channel 10`

if it's unknown hi-hat, use 150ms duration to decide if it's open or closed

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --maxhh 150`

print SFZ soundfont

`wavescan -d /audio/Drums/5Pin --sfz > ~/home/Music/SFZ/5Pin.sfz`

the same but with extended midi key syntax

`wavescan -d /audio/Drums/5Pin --sfz --sfz-mk > ~/home/Music/SFZ/5Pin.sfz`
