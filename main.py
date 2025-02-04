from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import json
import time
import os
from loguru import logger

# Şehir ve ilçe verilerini JSON'dan yükleme
def load_cities_and_districts():
    try:
        with open("cities_districts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Hata", "Şehir ve ilçe dosyası bulunamadı.")
        return {}

cities = load_cities_and_districts()

# Kategori listesini JSON'dan yükleme
def load_categories():
    try:
        with open("categories.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        messagebox.showerror("Hata", "Kategori dosyası bulunamadı.")
        return []

categories = load_categories()

# Kullanıcıdan seçilen bilgiler
def fetch_data():
    city = city_combobox.get()
    district = district_combobox.get()
    category = category_combobox.get()
    search_name = search_name_entry.get().strip()

    if not city or not district or not category:
        messagebox.showerror("Hata", "Lütfen tüm kriterleri seçin.")
        return

    if not search_name:
        messagebox.showerror("Hata", "Lütfen bir arama ismi girin.")
        return

    selected_fields = [field for field, var in field_vars.items() if var.get()]
    if not selected_fields:
        messagebox.showerror("Hata", "Lütfen Excel'e aktarılacak en az bir alan seçin.")
        return

    query = f"{category} {district} {city}"
    print(f"Arama sorgusu: {query}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    try:
        driver.get(f"https://www.google.com/search?q={query}&tbm=lcl")
        time.sleep(3)

        data = []

        for _ in range(2):  # Varsayılan sayfa sayısı
            html_main_page = driver.page_source
            soup = BeautifulSoup(html_main_page, 'html.parser')
            elements = soup.find_all(attrs={"jscontroller": "AtSb"})
            ids = [element.get('id') for element in elements]

            print(f"Bulunan eleman sayısı: {len(ids)}")

            for b_id in ids:
                try:
                    business_tag = driver.find_element(By.XPATH, f'//*[@id="{b_id}"]')
                    business_tag.click()
                    time.sleep(3)

                    html = driver.page_source
                    soup_phone = BeautifulSoup(html, 'html.parser')

                    a = soup.find("div", id=b_id)
                    star = a.find("span", class_="yi40Hd YrbPuc").text if a.find("span", class_="yi40Hd YrbPuc") else 'N/A'
                    review = a.find('span', class_='RDApEe YrbPuc').text.strip('()') if a.find('span', class_='RDApEe YrbPuc') else 'N/A'

                    phone_tag = soup_phone.find('a', {'data-dtype': 'd3ph'})
                    phone_number = phone_tag.find('span').text.strip() if phone_tag and phone_tag.find('span') else 'N/A'
                    business_name = soup_phone.find('h2', {'data-attrid': 'title'}).find('span').text.strip() if soup_phone.find('h2', {'data-attrid': 'title'}) else 'N/A'
                    address_span = soup_phone.find('span', class_='LrzXr').text.strip() if soup_phone.find('span', class_='LrzXr') else 'N/A'

                    logger.success(f"{business_name}, {address_span}, {phone_number}, {star}, {review}")

                    record = {
                        "İşletme İsmi": business_name,
                        "Adres": address_span,
                        "Telefon": phone_number,
                        "Yıldız": star,
                        "Değerlendirme Sayısı": review
                    }
                    data.append(record)

                except Exception as e:
                    logger.error(f"Bir hata oluştu: {e}")

            try:
                next_button = driver.find_element(By.XPATH, '//*[@id="pnnext"]')
                next_button.click()
                time.sleep(5)
            except Exception as e:
                print(f"Bir hata oluştu (sonraki sayfa yüklenemedi): {e}")
                break

        if not data:
            messagebox.showinfo("Bilgi", "Hiçbir sonuç bulunamadı.")
            return

        # Dosya yazma işlemi
        file_path = os.path.join(os.getcwd(), f"{search_name}.xlsx")
        try:
            df = pd.DataFrame(data)
            df.to_excel(file_path, index=False)
            logger.warning(f"Veriler '{file_path}' dosyasına kaydedildi.")
        except PermissionError:
            messagebox.showerror("Hata", "Dosya zaten açık veya yazma izni yok.")

    except Exception as e:
        logger.error(f"Bir hata oluştu (genel hata): {e}")
        messagebox.showerror("Hata", "Arama işlemi sırasında bir hata oluştu.")

    finally:
        driver.quit()

# GUI başlat
root = tk.Tk()
root.title("İşletme Arama Botu")
root.geometry("400x550")
root.resizable(False, False)

frame = ttk.Frame(root, padding="15")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Şehir seçimi
ttk.Label(frame, text="Şehir:").grid(row=0, column=0, sticky=tk.W, pady=5)
city_combobox = ttk.Combobox(frame, values=list(cities.keys()), width=25)
city_combobox.grid(row=0, column=1, pady=5, sticky=tk.EW)

# İlçe seçimi
ttk.Label(frame, text="İlçe:").grid(row=1, column=0, sticky=tk.W, pady=5)
district_combobox = ttk.Combobox(frame, width=25)
district_combobox.grid(row=1, column=1, pady=5, sticky=tk.EW)

city_combobox.bind("<<ComboboxSelected>>", lambda e: district_combobox.config(values=cities.get(city_combobox.get(), [])))

# Kategori seçimi
ttk.Label(frame, text="Kategori:").grid(row=2, column=0, sticky=tk.W, pady=5)
category_combobox = ttk.Combobox(frame, values=categories, width=25)
category_combobox.grid(row=2, column=1, pady=5, sticky=tk.EW)

# Arama ismi girişi
ttk.Label(frame, text="Arama İsmi:").grid(row=3, column=0, sticky=tk.W, pady=5)
search_name_entry = ttk.Entry(frame, width=25)
search_name_entry.grid(row=3, column=1, pady=5, sticky=tk.EW)

# Excel alanları
fields_frame = ttk.LabelFrame(frame, text="Excel'e Aktarılacak Alanlar", padding="10")
fields_frame.grid(row=4, column=0, columnspan=2, pady=10, sticky=tk.EW)

field_vars = {
    "İşletme İsmi": tk.BooleanVar(value=True),
    "Adres": tk.BooleanVar(value=True),
    "Telefon": tk.BooleanVar(value=True)
}

for idx, (field, var) in enumerate(field_vars.items()):
    ttk.Checkbutton(fields_frame, text=field, variable=var).grid(row=idx, column=0, sticky=tk.W)

# Çalıştır butonu
ttk.Button(frame, text="Ara ve Kaydet", command=fetch_data).grid(row=5, column=0, columnspan=2, pady=10, sticky=tk.EW)

root.mainloop()
