import argparse
from .range_helper import float_range

def create_basic_parser() -> argparse.ArgumentParser:
    """
    Temel argüman ayrıştırıcıyı oluşturur.
    
    Returns:
        argparse.ArgumentParser: Temel argümanları içeren ayrıştırıcı
    """
    parser = argparse.ArgumentParser(description="WhatsApp tarzı QR kod oluşturucu")
    parser.add_argument("data", help="QR kodunda yer alacak veri")
    parser.add_argument("-o", "--output", help="Çıktı dosyasının adı (örn: qrcode.png)", default="karekod.png")
    return parser

def add_appearance_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Görünüm ile ilgili argümanları ekler.
    
    Args:
        parser (argparse.ArgumentParser): Mevcut argüman ayrıştırıcı

    Returns:
        None
    """
    parser.add_argument("-t", "--title", help="QR kodun üstüne eklenecek başlık", default="WhatsApp QR Kodu")
    parser.add_argument("-tc", "--title_color", type=str, help="Başlık rengi", default="black")
    parser.add_argument("-r", "--resolution", type=int, help="QR kodun çözünürlüğü (piksel cinsinden genişlik)", default=1080)
    parser.add_argument("-f", "--format", help="Çıktı dosyası formatı (png, jpg, bmp, vb.)", default="png")
    parser.add_argument(
        "-fgc", "--foreground_color", 
        type=str, 
        help="QR kodun ön plan rengi (modüllerin rengi). Örnekler: black (siyah), darkblue (koyu mavi), darkgreen (koyu yeşil), brown (kahverengi), purple (mor)", 
        default="black"
    )
    parser.add_argument(
        "-bgc", "--background_color", 
        type=str, 
        help="QR kodun arka plan rengi (arka planın rengi). Örnekler: white (beyaz), lightgray (açık gri), lightyellow (açık sarı), lightblue (açık mavi), lightgreen (açık yeşil)", 
        default="white"
    )


def add_image_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Resim ile ilgili argümanları ekler.
    
    Args:
        parser (argparse.ArgumentParser): Mevcut argüman ayrıştırıcı

    Returns:
        None
    """
    parser.add_argument("-i", "--images", nargs='+', help="Eklenecek resim dosyalarının yolları", default=None)
    parser.add_argument("-ts", "--text_scale_factor", type=float, help="Yazının boyutu (tavsiye edilen 1)", default=1.0)
    parser.add_argument("-ls", "--logo_scale_factor", type=float, help="Logoların boyutu (tavsiye edilen 1)", default=1.0)

def add_qr_version_arguments(parser: argparse.ArgumentParser) -> None:
    """
    QR kod versiyonu ile ilgili argümanları ekler.
    
    Args:
        parser (argparse.ArgumentParser): Mevcut argüman ayrıştırıcı

    Returns:
        None
    """
    parser.add_argument("-mv", "--min_version", type=int, help="Minimum QR kod versiyonu (1-40 arası)", default=1, choices=range(1, 41))
    parser.add_argument("-xv", "--max_version", type=int, help="Maksimum QR kod versiyonu (1-40 arası)", default=20, choices=range(1, 41))

def add_center_logo_arguments(parser: argparse.ArgumentParser) -> None:
    """
    Merkez logo ile ilgili argümanları ekler.
    
    Args:
        parser (argparse.ArgumentParser): Mevcut argüman ayrıştırıcı

    Returns:
        None
    """
    parser.add_argument("-cl", "--center_logo", help="QR kodun merkezine yerleştirilecek logo dosyasının yolu", default=None)
    parser.add_argument("-cls", "--center_logo_size", help="QR kodun merkezine yerleştirilecek logonun boyuta oranı (0-1 arası)", type=float_range, default=0.2)
    parser.add_argument("-ilc", "--is_logo_circle", action="store_true", help="Merkez logonun daire şeklinde olup olmayacağı", default=False)
    parser.add_argument("-bs", "--border_size", type=float, help="Merkez logonun kenarlık boyutu (en fazla 0.15 önerilir)", default=0.0)
    parser.add_argument("-bc", "--border_color", help="Merkez logonun kenarlık rengi", default="white")

def create_argument_parser() -> argparse.ArgumentParser:
    """
    Tüm argümanları içeren tam bir argüman ayrıştırıcı oluşturur.
    
    Returns:
        argparse.ArgumentParser: Tüm argümanları içeren ayrıştırıcı
    """
    parser = create_basic_parser()
    add_appearance_arguments(parser)
    add_image_arguments(parser)
    add_qr_version_arguments(parser)
    add_center_logo_arguments(parser)
    return parser

def is_version_valid(min_version: float, max_version: float) -> bool:
    """
    Minimum ve maksimum versiyon değerlerinin geçerliliğini kontrol eder.

    Args:
        min_version (float): Minimum versiyon değeri
        max_version (float): Maksimum versiyon değeri

    Returns:
        bool: Versiyon değerleri geçerliyse True, değilse False
    """
    return min_version <= max_version

def is_border_size_valid(border_size: int) -> bool:
    """
    Kenarlık boyutunun geçerliliğini kontrol eder.

    Args:
        border_size (int): Kenarlık boyutu

    Returns:
        bool: Kenarlık boyutu geçerliyse True, değilse False
    """
    return border_size >= 0

def is_arguments_valid(args: argparse.Namespace, parser: argparse.ArgumentParser) -> bool:
    """
    Argümanların geçerliliğini kontrol eder.
    
    Args:
        args (argparse.Namespace): Ayrıştırılmış argümanlar
        parser (argparse.ArgumentParser): Argüman ayrıştırıcı
    
    Returns:
        bool: Argümanlar geçerliyse True, değilse False
    """
    if not is_version_valid(args.min_version, args.max_version):
        parser.error("Minimum versiyon, maksimum versiyondan büyük olamaz.")
        return False
    
    if not is_border_size_valid(args.border_size):
        parser.error("Kenarlık boyutu negatif olamaz.")
        return False
    
    return True
