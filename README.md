# prepare LSP multisampler config from sample files

Find all wav/flac/aif samples in provided with `-d` directory and print text config for importing to [LSP multisampler](https://lsp-plug.in/?page=manuals). Debug messages are printing to stderr.

## requirements

python 3 with couple of modules

```bash
pip install audiofile
pip install Jinja2
```

## examples

scan directory tree for samples, store config in 'dk900.cfg'

`wavescan -d /audio/H2/Roland_TB909Kit --lsp > dk909.cfg`

print debug messages and add comments to config  (`-D`), also respect LSP limits (`--limit`) with max 48 instruments and 8 samples per each

`wavescan -d /audio/Drums/KITS/KIT_TECH/ --lsp -D --limit  > SFZ_TECH.cfg`

use MIDI channel 10 instead of default 1

`wavescan -d /audio/Drums/BespokeLiveDrums/Electric/ --lsp --channel 10`

also we have help

```text
wavescan --help
usage: wavescan [-h] -d DIR [--channel CHANNEL] [--lsp] [-D] [--limit]

optional arguments:
  -h, --help         show this help message and exit
  -d DIR, --dir DIR  samples directory
  --channel CHANNEL  MIDI channel (1-16)
  --lsp              LSP multisampler output
  -D                 Debug output
  --limit            Respect LSP limits and skip extra data
```
