# vinyllabel - create labels from ID3 tags

This program reads meta data from aiff audio files. The audio stream waveform picture will be rendered into a png image. Album, track information and the waveform picture can be freely used in templated html files.

![example](test/demo/example.png)

## Installation

Following dependencies need to be fullfilled.

```python
pip install mutagen
pip install jinja2
pip install pydub
pip install Pillow
```

## Usage

```python
vinyllabel.py [-h] [--template T] [--debug D] PATH
```

## Configuration

Using `conf/config.json` you are free to map ID3 meta tags on to keys. Each key will be present in the jinja2 html template. Use `--debug` argument to print all tags present in a media file.

```json
"keymapping": {
        "album": {
            "name": "TALB",
            "artist": "TPE2",
            "publisher": "TPUB",
            "country": "TXXX:COUNTRY",
            "year": "TDRC"
        },
        "track": {
            "pos": "TRCK",
            "title": "TIT2",
            "artist": "TPE1",
            "key": "TKEY",
            "genre": "TCON",
            "bpm": "TBPM",
            "rpm": "TXXX:TMT/TT",
            "energy": "TXXX:EnergyLevel"
        }
    }
```
Tag content can be modified freely by regular expressions. In this example key and bpm are getting removed from the track title.

```json
    "regex": {
        "track": {
            "title": "^[0-9]+[a-zA-Z]+ - [0-9]+ - (.*)$"
        }
    }
```
