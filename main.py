import argparse
from helpers import create_whatsapp_qr

def main() -> None:
    """
    WhatsApp tarzı QR kod oluşturucu için komut satırı arayüzü.

    Returns:
        None
    """
    parser = argparse.ArgumentParser(description="WhatsApp tarzı QR kod oluşturucu")
    parser.add_argument("data", help="QR kodunda yer alacak veri")
    parser.add_argument("-o", "--output", help="Çıktı dosyasının adı (örn: qrcode.png)", default="karekod.png")
    parser.add_argument("-t", "--title", help="QR kodun üstüne eklenecek başlık", default="WhatsApp QR Kodu")
    parser.add_argument("-i", "--images", nargs='+', help="Eklenecek resim dosyalarının yolları", default=None)
    parser.add_argument("-r", "--resolution", type=int, help="QR kodun çözünürlüğü (piksel cinsinden genişlik)", default=1080)
    parser.add_argument("-f", "--format", help="Çıktı dosyası formatı (png, jpg, bmp, vb.)", default="png")
    parser.add_argument("-ts", "--text_scale_factor", type=float, help="Yazının boyutu (tavsiye edilen 1)", default=1.0)
    parser.add_argument("-ls", "--logo_scale_factor", type=float, help="Logoların boyutu (tavsiye edilen 1)", default=1.0)
    parser.add_argument("-mv", "--min_version", type=int, help="Minimum QR kod versiyonu (1-40 arası)", default=1, choices=range(1, 41))
    parser.add_argument("-xv", "--max_version", type=int, help="Maksimum QR kod versiyonu (1-40 arası)", default=20, choices=range(1, 41))
    parser.add_argument("-cl", "--center_logo", help="QR kodun merkezine yerleştirilecek logo dosyasının yolu", default=None)
    parser.add_argument("-ilc", "--is_logo_circle", action="store_true", help="Merkez logonun daire şeklinde olup olmayacağı", default=False)
    parser.add_argument("-bs", "--border_size", type=float, help="Merkez logonun kenarlık boyutu (en fazla 0.15 önerilir)", default=0.0)
    parser.add_argument("-bc", "--border_color", help="Merkez logonun kenarlık rengi", default="white")

    args = parser.parse_args()

    if args.min_version > args.max_version:
        parser.error("Minimum versiyon, maksimum versiyondan büyük olamaz.")
    
    if args.border_size < 0:
        parser.error("Kenarlık boyutu negatif olamaz.")

    create_whatsapp_qr(args.data, args.output, args.title, args.resolution, args.images, args.format,
                       args.text_scale_factor, args.logo_scale_factor, args.min_version, args.max_version,
                       args.center_logo, args.is_logo_circle, args.border_size, args.border_color)

if __name__ == "__main__":
    main()

