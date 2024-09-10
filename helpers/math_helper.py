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
    return sum(font.getbbox(line)[3] - font.getbbox(line)[1] for line in wrapped_text)

def calculate_dimensions(scale_factor: float, img_h: int) -> Tuple[int, int, int, int]:
    """
    Arka plan için gerekli boyutları hesaplar.

    Args:
        scale_factor (float): Ölçeklendirme faktörü.
        img_h (int): QR kod görüntüsünün yüksekliği.

    Returns:
        Tuple[int, int, int, int]: Kenar boşluğu, maksimum başlık yüksekliği, boşluk ve maksimum logo boyutu.
    """
    margin = int(50 * scale_factor)
    max_title_height = int(120 * scale_factor)
    spacing = int(5 * scale_factor)
    logo_max_size = int(50 * scale_factor)
    return margin, max_title_height, spacing, logo_max_size