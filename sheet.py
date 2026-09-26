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

    filename = os.path.basename(video_filepath)

    utils.log_done(filename, "file's metadata is extracted")

    video_tiles = commands.extract_tiles(
        video_filepath, rows * cols, video_stream.duration
    )

    meta_pairs = [
        ("Filename", filename),
        ("Resolution", f"{video_stream.width}x{video_stream.height}"),
        ("Coded Resolution", f"{video_stream.coded_width}x{video_stream.coded_height}"),
        ("Duration", get_duration_string(video_stream.duration)),
        ("Video Codec", f"{video_stream.codec_name} {video_stream.profile}"),
        ("Frame Rate", f"{video_stream.frame_rate:.2f} fps"),
        ("Pixel Format", video_stream.pix_fmt),
        ("Color Space", video_stream.color_space),
        (
            "Audio",
            f"{audio_stream.codec_name} {audio_stream.sample_rate} {audio_stream.channels} Channels",
        ),
    ]

    line_h = font_meta.size + 4
    header_h = margin + len(meta_pairs) * line_h + margin  # metadata height

    grid_w = cols * tile[0] + (cols - 1) * gap
    grid_h = rows * tile[1] + (rows - 1) * gap

    width = margin * 2 + grid_w  # total output width
    height = margin * 2 + header_h + seperator_gap + grid_h  # total output height

    canvas = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)

    metadata.draw_metadata(meta_pairs, draw, margin, line_h, font_meta)

    sep_y = margin + header_h + seperator_gap // 2
    draw.line(
        [(margin, sep_y), (width - margin, sep_y)], fill=(255, 255, 255, 80), width=1
    )

    tile_start_h = margin + header_h + seperator_gap

    tiles.draw_tiles_block(
        video_tiles,
        canvas,
        tile_start_h,
        margin,
        tile[0],
        tile[1],
        cols,
        gap,
    )

    canvas.save(save_filepath, format="PNG")

    console.print(
        f"[bold green]✔[/] [bold]{save_filepath}[/] [dim] {width}x{height} output file is saved[/]",
        highlight=False,
    )

    print(" Metadata of the video file ".center(64, "-"))

    label_w = max(len(label) for label, _ in meta_pairs)
    for label, value in meta_pairs:
        print(f"{label:<{label_w}} : {value}")
