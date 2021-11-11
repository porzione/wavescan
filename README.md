# wavescan - scan directories for wav/flac drum samples and build LSP Plugins multisampler config

## requirements

```
pip install audiofile
pip install Jinja2
```

## examples

`wavescan -d /audio/H2/Roland_TB909Kit --lsp -D > dk909.cfg` scan directory tree for samples

flag `--limit` respect LSP limits, max 48 instruments with max 8 samples each

`wavescan --help` - obviously
