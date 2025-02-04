@echo off

:: Python kütüphanelerini yüklemek için bir sanal ortam oluşturuluyor
python -m venv venv

:: Sanal ortamı etkinleştirme
call venv\Scripts\activate

:: Gerekli Python kütüphanelerini yükleme
echo Gerekli kütüphaneler yükleniyor...
pip install --upgrade pip
pip install selenium
pip install beautifulsoup4
pip install pandas
pip install openpyxl
pip install loguru
pip install webdriver-manager

echo Kütüphaneler başarıyla yüklendi!

deactivate

:: İşlem tamamlandıktan sonra bekleme
pause
