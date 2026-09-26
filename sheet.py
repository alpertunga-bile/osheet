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


def get_duration_string(duration: float) -> str:
    pruned_duration = int(duration)

    hours = pruned_duration // 3600
    minutes = (pruned_duration - hours * 3600) // 60
    seconds = pruned_duration - hours * 3600 - minutes * 60

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def create_sheet(
    video_filepath: str,
    font_meta: ImageFont.FreeTypeFont,
    save_filepath: str,
    rows: int,
    cols: int,
    tile: tuple[int, int],
    gap: int,
    margin: int,
    seperator_gap: int,
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

    video_tiles = commands.extract_tiles(
        video_filepath, rows * cols, video_stream.duration
    )

    meta_lines = [
        f"Filename : {os.path.basename(video_filepath)}",
        f"Resolution : {video_stream.width}x{video_stream.height}",
        f"Coded Resoulution : {video_stream.coded_width}x{video_stream.coded_height}",
        f"Duration : {get_duration_string(video_stream.duration)}",
        f"Video Codec : {video_stream.codec_name} {video_stream.profile}",
        f"Frame Rate : {video_stream.frame_rate:.2f} fps",
        f"Pixel Format : {video_stream.pix_fmt}",
        f"Color Space : {video_stream.color_space}",
        f"Audio : {audio_stream.codec_name} {audio_stream.sample_rate} {audio_stream.channels} Channels",
    ]

    line_h = font_meta.size + 4
    header_h = margin + len(meta_lines) * line_h + margin  # text band height

    grid_w = cols * tile[0] + (cols - 1) * gap
    grid_h = rows * tile[1] + (rows - 1) * gap

    width = margin * 2 + grid_w
    height = margin * 2 + header_h + seperator_gap + grid_h

    canvas = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)

    metadata.draw_metadata(meta_lines, draw, margin, line_h, font_meta)

    sep_y = margin + header_h + seperator_gap // 2
    draw.line(
        [(margin, sep_y), (width - margin, sep_y)], fill=(255, 255, 255, 80), width=1
    )

    tiles.draw_tiles_block(
        video_tiles,
        canvas,
        margin,
        header_h,
        seperator_gap,
        tile[1],
        tile[0],
        cols,
        gap,
    )

    canvas.save(save_filepath, format="PNG")

    console.print(
        f"[bold green]✔[/] [bold]{save_filepath}[/] [dim] {width}x{height} output file is saved[/]",
        highlight=False,
    )

    print(" Metadata of the video file ".center(64, "-"))

    for line in meta_lines:
        print(line)
