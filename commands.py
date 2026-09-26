import json
import os
import subprocess
import sys

from rich.progress import track

import infos
import utils


def run_cmd(command: list[str]) -> tuple[bool, bytes]:
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            shell=False,
            check=False,
            timeout=180,
            stdin=subprocess.DEVNULL,
        )
    except (OSError, subprocess.SubprocessError) as error:
        utils.log_error("commands.py", f"cannot run {command}")
        return (False, b"")

    if 0 != result.returncode:
        print("The run command is failed")
        print(f"Command: {command}")
        print("# --------------------------------------------------------------- #")
        print(str(result.stderr))
        print("# --------------------------------------------------------------- #")
        return (False, b"")

    return (True, result.stdout)


def get_stream_infos(
    filepath: str,
) -> tuple[infos.VideoStreamInfo, infos.AudioStreamInfo]:
    video_stream = infos.get_default_video_stream_info()
    audio_stream = infos.get_default_audio_stream_info()

    if os.path.exists(filepath) is False:
        utils.log_error(filepath, "doesnot exist")
        return (video_stream, audio_stream)

    is_success, result = run_cmd(
        [
            "ffprobe",
            "-v",
            "error",
            "-print_format",
            "json",
            "-show_format",
            "-show_streams",
            filepath,
        ]
    )

    if is_success is False:
        return (video_stream, audio_stream)

    try:
        stream_json = json.loads(result)
    except json.JSONDecodeError:
        utils.log_error(filepath, "ffprobe output cannot be parsed")
        return (video_stream, audio_stream)

    streams = stream_json["streams"]

    for stream in streams:
        codec_type = stream["codec_type"]

        if "video" == codec_type:
            video_stream = infos.create_video_stream_info(stream)
        elif "audio" == codec_type:
            audio_stream = infos.create_audio_stream_info(stream)

    if 0.0 == video_stream.duration:
        video_stream.duration = infos.json_get_float_val_or_default(
            stream_json["format"], "duration", 0.0
        )

    return (video_stream, audio_stream)


def extract_tiles(
    video_filepath: str,
    n_tiles: int,
    duration: float,
    tile_w: int = 320,
    out_dir: str = "temp",
) -> list[str]:
    os.makedirs("temp", exist_ok=True)
    tiles = []

    for i in track(range(n_tiles), description="Extracting video frames"):
        t = duration * i / n_tiles
        filename = f"tile_{i:03d}.png"
        tile = f"{out_dir}/{filename}"

        is_success, _ = run_cmd(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-ss",
                f"{t:.3f}",  # fast seek BEFORE -i
                "-i",
                video_filepath,
                "-frames:v",
                "1",
                "-vf",
                f"scale={tile_w}:-2",
                "-f",
                "image2",
                "-y",  # overwrite without prompting
                str(tile),
            ]
        )

        if is_success:
            tiles.append(tile)
        else:
            print(f"The extracting operation for {i + 1} is failed")
            sys.exit(1)

    return tiles
