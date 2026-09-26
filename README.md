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

| Argument Name | Default Value | Description |
| :-----------: | :-----------: | :---------- |
| --input; -i   | **required**    | Real or relative path of the video file |  
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