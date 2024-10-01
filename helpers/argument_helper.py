import argparse
from .range_helper import float_range


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="WhatsApp tarzı QR kod oluşturucu")
    parser.add_argument("data", help="QR kodunda yer alacak veri")
    parser.add_argument("-o", "--output", help="Çıktı dosyasının adı (örn: qrcode.png)", default="karekod.png")
    parser.add_argument("-t", "--title", help="QR kodun üstüne eklenecek başlık", default="WhatsApp QR Kodu")
    parser.add_argument("-tc", "--title_color", type=str, help="Başlık rengi", default="black")
    parser.add_argument("-i", "--images", nargs='+', help="Eklenecek resim dosyalarının yolları", default=None)
    parser.add_argument("-r", "--resolution", type=int, help="QR kodun çözünürlüğü (piksel cinsinden genişlik)", default=1080)
    parser.add_argument("-f", "--format", help="Çıktı dosyası formatı (png, jpg, bmp, vb.)", default="png")
    parser.add_argument("-ts", "--text_scale_factor", type=float, help="Yazının boyutu (tavsiye edilen 1)", default=1.0)
    parser.add_argument("-ls", "--logo_scale_factor", type=float, help="Logoların boyutu (tavsiye edilen 1)", default=1.0)
    parser.add_argument("-mv", "--min_version", type=int, help="Minimum QR kod versiyonu (1-40 arası)", default=1, choices=range(1, 41))
    parser.add_argument("-xv", "--max_version", type=int, help="Maksimum QR kod versiyonu (1-40 arası)", default=20, choices=range(1, 41))
    parser.add_argument("-cl", "--center_logo", help="QR kodun merkezine yerleştirilecek logo dosyasının yolu", default=None)
    parser.add_argument("-cls", "--center_logo_size", help="QR kodun merkezine yerleştirilecek logonun boyuta oranı (0-1 arası)", type=float_range, default=0.2)
    parser.add_argument("-ilc", "--is_logo_circle", action="store_true", help="Merkez logonun daire şeklinde olup olmayacağı", default=False)
    parser.add_argument("-bs", "--border_size", type=float, help="Merkez logonun kenarlık boyutu (en fazla 0.15 önerilir)", default=0.0)
    parser.add_argument("-bc", "--border_color", help="Merkez logonun kenarlık rengi", default="white")
    return parser


def is_arguments_valid(args: argparse.Namespace, parser: argparse.ArgumentParser) -> bool:
    if args.min_version > args.max_version:
        parser.error("Minimum versiyon, maksimum versiyondan büyük olamaz.")
        return False
    if args.border_size < 0:
        parser.error("Kenarlık boyutu negatif olamaz.")
        return False
    return True