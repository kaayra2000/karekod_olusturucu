#!/bin/bash

# Sanal ortam adı
VENV_NAME="qr_code_env"

# Python'un yüklü olup olmadığını kontrol et
if ! command -v python3 &> /dev/null
then
    echo "Python3 yüklü değil. Yükleniyor..."
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        case $ID in
            ubuntu|debian)
                sudo apt-get update
                sudo apt-get install -y python3 python3-pip python3-venv
                ;;
            fedora|centos|rhel)
                sudo dnf install -y python3 python3-pip python3-virtualenv
                ;;
            *)
                echo "Desteklenmeyen işletim sistemi. Lütfen Python3'ü manuel olarak yükleyin."
                exit 1
                ;;
        esac
    else
        echo "İşletim sistemi belirlenemedi. Lütfen Python3'ü manuel olarak yükleyin."
        exit 1
    fi
fi

# Sanal ortamın var olup olmadığını kontrol et
if [ ! -d "$VENV_NAME" ]; then
    echo "Sanal ortam bulunamadı. Yeni bir sanal ortam oluşturuluyor..."
    python3 -m venv $VENV_NAME
else
    echo "Sanal ortam zaten mevcut."
fi

# Sanal ortamı etkinleştir
source $VENV_NAME/bin/activate
pip install --upgrade pip

# requirements.txt dosyasından paketleri kontrol et ve gerekirse yükle
while read requirement; do
    echo "Gereksinim kontrol ediliyor: $requirement"
    if pip freeze | grep -i "^$requirement=" > /dev/null; then
        echo "$requirement zaten yüklü."
    else
        echo "$requirement yükleniyor..."
        pip install $requirement
    fi
done < requirements.txt

echo "Tüm gereksinimler kontrol edildi ve yüklendi."
echo "Sanal ortam etkinleştirildi: $VENV_NAME"
