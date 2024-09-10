from typing import List, Tuple
from PIL import ImageFont

def calculate_text_height(wrapped_text: List[str], font: ImageFont.ImageFont) -> int:
    """
    Sarılmış metnin toplam yüksekliğini hesaplar.

    Args:
        wrapped_text (List[str]): Sarılmış metin satırları.
        font (ImageFont.ImageFont): Kullanılan font.

    Returns:
        int: Metnin toplam yüksekliği.
    """
    return sum(calculate_line_height(line, font) for line in wrapped_text)

def calculate_line_height(line: str, font: ImageFont.ImageFont) -> int:
    """
    Tek bir metin satırının yüksekliğini hesaplar.

    Args:
        line (str): Metin satırı.
        font (ImageFont.ImageFont): Kullanılan font.

    Returns:
        int: Satırın yüksekliği.
    """
    left, top, right, bottom = font.getbbox(line)
    return bottom - top

def calculate_dimensions(scale_factor: float, img_h: int) -> Tuple[int, int, int, int]:
    """
    Arka plan için gerekli boyutları hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.
        img_h (int): QR kod görüntüsünün yüksekliği.

    Returns:
        Tuple[int, int, int, int]: Kenar boşluğu, maksimum başlık yüksekliği, boşluk ve maksimum logo boyutu.
    """
    return (
        calculate_margin(scale_factor),
        calculate_max_title_height(scale_factor),
        calculate_spacing(scale_factor),
        calculate_logo_max_size(scale_factor)
    )

def calculate_margin(scale_factor: float) -> int:
    """
    Kenar boşluğunu hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        int: Hesaplanan kenar boşluğu.
    """
    return int(50 * scale_factor)

def calculate_max_title_height(scale_factor: float) -> int:
    """
    Maksimum başlık yüksekliğini hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        int: Hesaplanan maksimum başlık yüksekliği.
    """
    return int(120 * scale_factor)

def calculate_spacing(scale_factor: float) -> int:
    """
    Boşluk miktarını hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        int: Hesaplanan boşluk miktarı.
    """
    return int(5 * scale_factor)

def calculate_logo_max_size(scale_factor: float) -> int:
    """
    Maksimum logo boyutunu hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.

    Returns:
        int: Hesaplanan maksimum logo boyutu.
    """
    return int(50 * scale_factor)
