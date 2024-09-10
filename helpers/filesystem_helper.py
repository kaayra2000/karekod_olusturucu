import os
from PIL import Image
from typing import Union
from .string_helper import create_versioned_filename
def save_qr_image(background: Union[Image.Image, object], output_file: str, version: int, output_format: str) -> None:
    """
    QR kod görüntüsünü belirtilen formatta ve sürüm numarasıyla kaydeder.

    Args:
        background (Union[Image.Image, object]): Kaydedilecek QR kod görüntüsü (PIL Image nesnesi veya benzer bir nesne).
        output_file (str): Kaydedilecek dosyanın yolu ve adı.
        version (int): QR kod sürüm numarası.
        output_format (str): Çıktı dosyasının formatı (örn. 'png', 'jpg').

    Returns:
        None: Fonksiyon bir değer döndürmez, ancak dosya sisteminde bir görüntü oluşturur.
    """
    output_dir = create_output_directory(output_file)
    versioned_output = create_versioned_filename(output_file, version, output_format, output_dir)

    try:
        background.save(versioned_output)
        print(f"QR kod versiyonu {version} başarıyla oluşturuldu ve {versioned_output} olarak kaydedildi.")
    except ValueError as e:
        print(f"Hata: {e}")
        print(f"QR kod versiyonu {version} kaydedilemedi. Lütfen geçerli bir format belirtin.")

def create_output_directory(output_file: str) -> str:
    """
    Çıktı dizinini oluşturur ve yolunu döndürür.

    Args:
        output_file (str): Kaydedilecek dosyanın yolu ve adı.

    Returns:
        str: Oluşturulan çıktı dizininin yolu.
    """
    output_dir = os.path.splitext(output_file)[0]
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

