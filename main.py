import argparse
from helpers import create_whatsapp_qr
from helpers.argument_helper import create_argument_parser, is_arguments_valid
def main() -> None:
    """
    WhatsApp tarzı QR kod oluşturucu için komut satırı arayüzü.

    Returns:
        None
    """
    parser = create_argument_parser() # argüman ayrıştırıcıyı oluştur

    args = parser.parse_args() # argümanları ayrıştır

    if not is_arguments_valid(args, parser): # argümanların geçerliliğini kontrol et
        return 1 # geçersiz argümanlar varsa hata kodu döndür

    create_whatsapp_qr(args.data, args.output, args.title, args.title_color, args.resolution, args.images, args.format,
                       args.text_scale_factor, args.logo_scale_factor, args.min_version, args.max_version,
                       args.center_logo, args.center_logo_size, args.is_logo_circle, args.border_size, args.border_color)

if __name__ == "__main__":
    main()

