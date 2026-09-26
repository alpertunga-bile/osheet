import math
import os
import time

from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

import commands
import infos
import metadata
import tiles
import utils

COLS = 4
TILE_W, TILE_H = 320, 180
GAP = 5  # spacing between tiles
MARGIN = 10  # outer margin
SEPARATOR_GAP = 8  # extra space between the two sections


def get_duration_string(duration: float) -> str:
    pruned_duration = int(duration)

    hours = pruned_duration // 3600
    minutes = (pruned_duration - hours * 3600) // 60
    seconds = pruned_duration - hours * 3600 - minutes * 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def create_sheet(
    video_filepath: str,
    font_meta: ImageFont.FreeTypeFont,
    n_tiles: int,
    save_filepath: str,
) -> None:
    console = Console()

    with console.status("Extracting metadata"):
        time.sleep(1.5)
        video_stream, audio_stream = commands.get_stream_infos(video_filepath)

    if infos.check_video_stream_empty(video_stream):
        utils.log_error(video_filepath, "cannot extract video metadata")
        return

    if infos.check_audio_stream_empty(audio_stream):
        utils.log_error(video_filepath, "cannot extract audio metadata")
        return

    utils.log_done(video_filepath, "file's metadata is extracted")

    video_tiles = commands.extract_tiles(video_filepath, n_tiles, video_stream.duration)

    meta_lines = [
        f"Filepath : {os.path.basename(video_filepath)}",
        f"Resolution : {video_stream.width}x{video_stream.height}",
        f"Coded Resoulution : {video_stream.coded_width}x{video_stream.coded_height}",
        f"Duration : {get_duration_string(video_stream.duration)}",
        f"Video Codec : {video_stream.codec_name.upper()} {video_stream.profile.upper()}",
        f"Frame Rate : {video_stream.frame_rate:.2f} fps",
        f"Pixel Format : {video_stream.pix_fmt.upper()}",
        f"Color Space : {video_stream.color_space.upper()}",
        f"Audio Codec : {audio_stream.codec_name.upper()}",
        f"Sample Rate : {audio_stream.sample_rate}",
        f"Channels : {audio_stream.channels} Channels",
    ]

    line_h = font_meta.size + 4
    header_h = MARGIN + len(meta_lines) * line_h + MARGIN  # text band height

    rows = math.ceil(n_tiles / COLS)
    grid_w = COLS * TILE_W + (COLS - 1) * GAP
    grid_h = rows * TILE_H + (rows - 1) * GAP

    W = MARGIN * 2 + grid_w
    H = MARGIN * 2 + header_h + SEPARATOR_GAP + grid_h

    canvas = Image.new("RGBA", (int(W), int(H)), (0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)

    metadata.draw_metadata(meta_lines, draw, MARGIN, line_h, font_meta)

    sep_y = MARGIN + header_h + SEPARATOR_GAP // 2
    draw.line([(MARGIN, sep_y), (W - MARGIN, sep_y)], fill=(255, 255, 255, 80), width=1)

    tiles.draw_tiles_block(
        video_tiles, canvas, MARGIN, header_h, SEPARATOR_GAP, TILE_H, TILE_W, COLS, GAP
    )

    canvas.save(save_filepath, format="PNG")

    console.print(
        f"[bold green]✔[/] [bold]{save_filepath}[/] [dim]output file is saved[/]",
        highlight=False,
    )
