import webcolors

def color_name_to_hex(color_name: str) -> str:
    """
    Verilen renk adını hexadecimal renk koduna dönüştürür.

    Args:
        color_name (str): Dönüştürülecek rengin adı

    Returns:
        str: Rengin hexadecimal kodu veya geçersiz renk adı durumunda None
    """
    try:
        hex_code = webcolors.name_to_hex(color_name)
        return hex_code
    except ValueError:
        print(f"'{color_name}' geçerli bir renk ismi değil.")
        return None

def hex_to_rgb(hex_color: str) -> tuple:
    """
    Hexadecimal renk kodunu RGB değerlerine dönüştürür.

    Args:
        hex_color (str): Dönüştürülecek hexadecimal renk kodu

    Returns:
        tuple: (R, G, B) formatında RGB değerleri
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
def get_rgb_from_color_name(color_name: str) -> tuple:
    """
    Verilen renk ismini alır ve karşılık gelen RGB tupılını döndürür.
    Eğer renk ismi geçersizse, ValueError fırlatır.

    Args:
        color_name (str): Renk ismi.

    Returns:
        tuple: RGB renk değeri tupılı.
    """
    # Renk ismini hex koduna dönüştür
    hex_code = color_name_to_hex(color_name)
    if hex_code is None:
        raise ValueError(f"Geçersiz renk ismi verildi. Hatayı düzeltin. Hatalı renk ismi: {color_name}")
    # Hex kodunu RGB tupılına dönüştür
    rgb_tuple = hex_to_rgb(hex_code)
    return rgb_tuple

