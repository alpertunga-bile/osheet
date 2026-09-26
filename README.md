# osheet

Create video contact sheet with metadata and thumbnails extracted from the video using ffmpeg and ffprobe.

## Requirements

- Python 3.x
- ffmpeg
- ffprobe
- Python packages under the **requirements.txt** file

## Usage

1. Create python virtual environment
```bash
python -m venv venv
```
2. With virtual environment's python executable install the required packages.
```bash
/venv/bin/python -m pip install requirements.txt
```
3. Run the script with wanted video's filepath
```bash
/venv/bin/python main.py -i sample.mp4
```

## CLI Arguments

```
❯ ./venv/bin/python main.py --help
usage: Create video contact sheet with rich metadata

options:
  -h, --help            show this help message and exit
  --input, -i INPUT     Input video filepath
  --font, -f FONT       Font type of the metadata
  --font_size, -fs FONT_SIZE
                        Size of the font of metadata
  --rows, -r ROWS       Total tile rows in the output
  --cols, -c COLS       Total tile columns in the output
  --tile_w, -tw TILE_W  Width of one tile
  --tile_h, -th TILE_H  Height of one tile
  --gap, -g GAP         Spacing between tiles
  --margin, -m MARGIN   Outer margin
  --sep_gap, -sg SEP_GAP
                        Extra space between text and tiles
  --output, -o OUTPUT   Output file
```

| Argument Name | Default Value | Description |
| :-----------: | :-----------: | :---------- |
| --input; -i   | *required*    | Real or relative path of the video file |  
| --font; -f    | DejaVuSans-Bold.ttf | Font type of the metadata |
| --font_size; -fs | 16 | Size of the font of the metadata |
| --rows; -r | 4 | Total tile rows of the tile grid |
| --cols; -c | 4 | Total tile columns of the tile grid |
| --tile_w; -tw | 320 | Width of the one tile |
| --tile_h; -th | 180 | Height of the one tile |
| --gap; -g | 5 | Spacing between tiles |
| --margin; -m | 10 | Outer margin |
| --sep_gap; -sg | 8 | Extra space between text and tile grid |
| --output; -o | sheet.png | Output filepath |