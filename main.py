import argparse
import os.path
import sys

from PIL import ImageFont

import sheet
import utils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "osheet", "Create video contact sheet with rich metadata"
    )
    parser.add_argument("--input", "-i", help="Input video filepath")
    parser.add_argument(
        "--font", "-f", default="DejaVuSans-Bold.ttf", help="Font type of the metadata"
    )
    parser.add_argument(
        "--font_size", "-fs", default=16, help="Size of the font of metadata"
    )
    parser.add_argument(
        "--rows", "-r", action="store", default=4, help="Total tile rows in the output"
    )
    parser.add_argument(
        "--cols",
        "-c",
        action="store",
        default=4,
        help="Total tile columns in the output",
    )
    parser.add_argument(
        "--tile_w", "-tw", action="store", default=320, help="Width of one tile"
    )
    parser.add_argument(
        "--tile_h", "-th", action="store", default=180, help="Height of one tile"
    )
    parser.add_argument(
        "--gap", "-g", action="store", default=5, help="Spacing between tiles"
    )
    parser.add_argument(
        "--margin", "-m", action="store", default=10, help="Outer margin"
    )
    parser.add_argument(
        "--sep_gap", "-sg", default=8, help="Extra space between text and tiles"
    )
    parser.add_argument("--output", "-o", default="sheet.png", help="Output file")

    args = parser.parse_args()

    if os.path.exists(args.input) is False:
        utils.log_error(args.input, "doesnot exist")
        sys.exit(1)

    font_meta = ImageFont.truetype(args.font, args.font_size)

    sheet.create_sheet(
        args.input,
        font_meta,
        args.output,
        int(args.rows),
        int(args.cols),
        (int(args.tile_w), int(args.tile_h)),
        int(args.gap),
        int(args.margin),
        int(args.sep_gap),
    )
