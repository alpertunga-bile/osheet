import dataclasses
import typing


def json_get_str_val_or_default(config: typing.Any, key: str, default: str = "") -> str:
    return str(config[key]) if config.get(key) else default


def json_get_int_val_or_default(config: typing.Any, key: str, default: int = 0) -> int:
    return int(config[key]) if config.get(key) else default


def json_get_float_val_or_default(
    config: typing.Any, key: str, default: float = 0
) -> float:
    return float(config[key]) if config.get(key) else default


@dataclasses.dataclass
class VideoStreamInfo:
    codec_name: str
    profile: str
    width: int
    height: int
    coded_width: int
    coded_height: int
    pix_fmt: str
    color_space: str
    frame_rate: float
    duration: float


def check_video_stream_empty(info: VideoStreamInfo) -> bool:
    return (
        0 == len(info.codec_name)
        and 0 == len(info.profile)
        and 0 == info.width
        and 0 == info.height
        and 0 == info.coded_width
        and 0 == info.coded_height
        and 0 == len(info.pix_fmt)
        and 0 == len(info.color_space)
        and 0.0 == info.frame_rate
        and 0.0 == info.duration
    )


def get_default_video_stream_info() -> VideoStreamInfo:
    return VideoStreamInfo(
        codec_name="",
        profile="",
        width=0,
        height=0,
        coded_width=0,
        coded_height=0,
        pix_fmt="",
        color_space="",
        frame_rate=0.0,
        duration=0.0,
    )


def create_video_stream_info(config: typing.Any) -> VideoStreamInfo:
    frame_rate = json_get_str_val_or_default(config, "r_frame_rate")

    calc_frame_rate = 0.0
    div_idx = frame_rate.find("/")

    if div_idx != -1:
        first_number, second_number = (
            int(frame_rate[:div_idx]),
            int(frame_rate[div_idx + 1 :]),
        )

        if second_number != 0:
            calc_frame_rate = first_number / second_number

    return VideoStreamInfo(
        codec_name=json_get_str_val_or_default(config, "codec_name"),
        profile=json_get_str_val_or_default(config, "profile"),
        width=json_get_int_val_or_default(config, "width"),
        height=json_get_int_val_or_default(config, "height"),
        coded_width=json_get_int_val_or_default(config, "coded_width"),
        coded_height=json_get_int_val_or_default(config, "coded_height"),
        pix_fmt=json_get_str_val_or_default(config, "pix_fmt"),
        color_space=json_get_str_val_or_default(config, "color_space"),
        frame_rate=calc_frame_rate,
        duration=json_get_float_val_or_default(config, "duration", 0.0),
    )


@dataclasses.dataclass
class AudioStreamInfo:
    codec_name: str
    profile: str
    sample_rate: int
    channels: int


def check_audio_stream_empty(info: AudioStreamInfo) -> bool:
    return (
        0 == len(info.codec_name)
        and 0 == len(info.profile)
        and 0 == info.sample_rate
        and 0 == info.channels
    )


def get_default_audio_stream_info() -> AudioStreamInfo:
    return AudioStreamInfo(codec_name="", profile="", sample_rate=0, channels=0)


def create_audio_stream_info(config: typing.Any) -> AudioStreamInfo:
    return AudioStreamInfo(
        codec_name=json_get_str_val_or_default(config, "codec_name"),
        profile=json_get_str_val_or_default(config, "profile"),
        sample_rate=int(json_get_str_val_or_default(config, "sample_rate", "0")),
        channels=json_get_int_val_or_default(config, "channels"),
    )
