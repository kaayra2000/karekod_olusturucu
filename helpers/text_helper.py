from typing import List, Tuple
from PIL import ImageFont
from .image_helper import load_font
import textwrap
from .math_helper import calculate_text_height
def wrap_text(title: str, font: ImageFont.ImageFont, max_width: int, max_height: int, scale_factor: float) -> Tuple[List[str], ImageFont.ImageFont]:
    """
    Metni belirli bir genişliğe ve yüksekliğe sığacak şekilde sarar ve gerekirse font boyutunu küçültür.

    Args:
        title (str): Sarılacak metin.
        font (ImageFont.ImageFont): Kullanılacak başlangıç fontu.
        max_width (int): Metnin sığması gereken maksimum genişlik.
        max_height (int): Metnin sığması gereken maksimum yükseklik.
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        Tuple[List[str], ImageFont.ImageFont]: Sarılmış metin satırları ve kullanılan font.
    """
    font_size = int(font.size)
    min_font_size = int(8 * scale_factor)

    while font_size > min_font_size:
        wrapped_text = wrap_text_to_width(title, font, max_width)
        if is_text_height_within_limit(wrapped_text, font, max_height):
            return wrapped_text, font
        font_size -= 1
        font = load_font(font_size, scale_factor)

    return [], font

def wrap_text_to_width(text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
    """
    Metni belirli bir genişliğe sığacak şekilde sarar.

    Args:
        text (str): Sarılacak metin.
        font (ImageFont.ImageFont): Kullanılacak font.
        max_width (int): Metnin sığması gereken maksimum genişlik.

    Returns:
        List[str]: Sarılmış metin satırları.
    """
    return textwrap.wrap(text, width=int(max_width / (font.size / 2)))

def is_text_height_within_limit(wrapped_text: List[str], font: ImageFont.ImageFont, max_height: int) -> bool:
    """
    Sarılmış metnin yüksekliğinin belirlenen limiti aşıp aşmadığını kontrol eder.

    Args:
        wrapped_text (List[str]): Sarılmış metin satırları.
        font (ImageFont.ImageFont): Kullanılan font.
        max_height (int): İzin verilen maksimum yükseklik.

    Returns:
        bool: Metin yüksekliği limiti aşmıyorsa True, aksi halde False.
    """
    total_height = sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)
    return total_height <= max_height

