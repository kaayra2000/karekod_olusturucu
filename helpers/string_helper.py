import os
def create_versioned_filename(output_file: str, version: int, output_format: str, output_dir: str) -> str:
    """
    Sürüm numarasını içeren dosya adını oluşturur.

    Args:
        output_file (str): Kaydedilecek dosyanın yolu ve adı.
        version (int): QR kod sürüm numarası.
        output_format (str): Çıktı dosyasının formatı.
        output_dir (str): Çıktı dizininin yolu.

    Returns:
        str: Oluşturulan sürümlü dosya adı.
    """
    base_filename = os.path.splitext(os.path.basename(output_file))[0]
    versioned_filename = f"{base_filename}_v{version}.{output_format}"
    return os.path.join(output_dir, versioned_filename)