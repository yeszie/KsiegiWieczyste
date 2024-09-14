import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

def find_and_click_button(button_text, numer_ksiegi):
    try:
        # Konfiguracja WebDrivera z użyciem webdriver_manager
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        # Otwieranie strony
        driver.get('https://przegladarka-ekw.ms.gov.pl/eukw_prz/KsiegiWieczyste/wyszukiwanieKW?komunikaty=true&kontakt=true&okienkoSerwisowe=false')
        
        # Czekanie na załadowanie strony
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="text"]'))
        )
        
        # Przeszukiwanie pól formularza
        input_elements = driver.find_elements(By.XPATH, '//input[@type="text"]')
        if len(input_elements) < 3:
            print("Nie znaleziono wystarczającej liczby pól tekstowych.")
            driver.quit()
            return
        
        # Zakładamy, że pierwsze trzy pola tekstowe to odpowiednie pola
        input_element_czesc1 = input_elements[0]
        input_element_czesc2 = input_elements[1]
        input_element_czesc3 = input_elements[2]
        
        # Wprowadzenie części numeru księgi wieczystej
        czesc1, czesc2, czesc3 = numer_ksiegi.split('/')
        input_element_czesc1.send_keys(czesc1)
        input_element_czesc2.send_keys(czesc2)
        input_element_czesc3.send_keys(czesc3)
        
        # Kliknięcie przycisku "Wyszukaj księgę"
        buttons = driver.find_elements(By.XPATH, '//input[@type="submit"] | //button')
        if not buttons:
            print("Nie znaleziono żadnych przycisków.")
        
        for button in buttons:
            button_text_attr = button.get_attribute('value') if button.tag_name == 'input' else button.text.strip()
            if button_text_attr and button_text_attr == button_text:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(button)
                )
                button.click()
                break

        # Czekanie na stronę wyników i przeszukiwanie przycisków
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'przyciskWydrukZwykly'))
        )
        
        # Próba kliknięcia przycisku "Przeglądanie aktualnej treści KW"
        button = driver.find_element(By.ID, 'przyciskWydrukZwykly')
        if button:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(button)
            )
            button.click()
        else:
            print("Nie znaleziono przycisku 'Przeglądanie aktualnej treści KW'.")

        # Czekanie na załadowanie treści strony docelowej
        time.sleep(10)

        # Pobranie treści HTML strony docelowej
        page_source = driver.page_source
        
        # Oczyszczanie treści HTML
        soup = BeautifulSoup(page_source, 'html.parser')
        
        # Usuwanie wszystkich tagów <script>
        for script in soup.find_all('script'):
            script.decompose()
        
        # Usuwanie wszystkich tagów <form>
        for form in soup.find_all('form'):
            form.decompose()
            
        # Usuwanie wszystkich tagów <meta>
        for meta in soup.find_all('meta'):
            meta.decompose()
            
        # Usuwanie wszystkich tagów <link>
        for link in soup.find_all('link'):
            link.decompose()
        
        # Usuwanie wszystkich tagów <head>
        for head in soup.find_all('head'):
            head.decompose()
        
        # Usuwanie tagu <table> z id "nawigacja"
        table_nawigacja = soup.find('table', {'id': 'nawigacja'})
        if table_nawigacja:
            table_nawigacja.decompose()
        
        # Zmieniamy znaki '/' na '_' w numerze księgi wieczystej do nazwy pliku
        file_name = numer_ksiegi.replace('/', '_') + '.html'
        file_path = os.path.join('html_output', file_name)
        
        # Sprawdzenie, czy katalog html_output istnieje
        os.makedirs('html_output', exist_ok=True)
        
        # Zapisanie treści do pliku
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))
        
        print(f"Treść strony została zapisana do pliku: {file_path}")
    except Exception as e:
        print(f"Wystąpił błąd przy przetwarzaniu numeru {numer_ksiegi}. Błąd: {e}")
    finally:
        # Zamknięcie przeglądarki
        driver.quit()

# Przetwarzanie numerów z pliku WA1G.txt
with open('WA1G.txt', 'r') as file:
    for numer_ksiegi in file:
        numer_ksiegi = numer_ksiegi.strip()
        if not numer_ksiegi:
            continue

        # Sprawdzenie, czy plik HTML już istnieje
        file_name = numer_ksiegi.replace('/', '_') + '.html'
        file_path = os.path.join('html_output', file_name)
        if os.path.exists(file_path):
            print(f"Plik {file_path} już istnieje, pomijam zapytanie.")
            continue

        # Wywołanie funkcji find_and_click_button
        find_and_click_button("WYSZUKAJ KSIĘGĘ", numer_ksiegi)
        print("wait 1s")
        time.sleep(1)