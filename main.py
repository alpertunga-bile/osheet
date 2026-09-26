from PIL import ImageFont
import sheet
from rich.prompt import Prompt
import re


def clean_path(raw: str) -> str:
    raw = raw.strip().strip('"')  # tolerate surrounding quotes
    raw = re.sub(r"\\([\[\]])", r"\1", raw)  # NBQ\[XC\] -> NBQ[XC]
    return raw


if __name__ == "__main__":
    filepath = clean_path(Prompt.ask("Video filepath"))

    font_meta = ImageFont.truetype("DejaVuSans-Bold.ttf", 16)

    n_tiles = Prompt.ask("Total tiles", choices=["12", "16", "20"], default="16")

    save_filepath = Prompt.ask("Save filepath", default="sheet.png")

    sheet.create_sheet(filepath, font_meta, int(n_tiles), save_filepath)
