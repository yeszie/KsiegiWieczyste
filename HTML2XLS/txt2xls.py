import pandas as pd
import json
import os
from datetime import datetime

# Funkcja do usuwania pierwszej i ostatniej linii z pliku
def remove_first_and_last_lines(file_path):
    temp_file_path = file_path + '.temp'
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    if len(lines) > 2:  # Sprawdź, czy jest więcej niż 2 linie
        with open(temp_file_path, 'w', encoding='utf-8') as file:
            file.writelines(lines[1:-1])  # Zapisz wszystkie linie z wyjątkiem pierwszej i ostatniej

    return temp_file_path

# Funkcja do usuwania plików tymczasowych
def delete_temp_files(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt.temp'):
            temp_file_path = os.path.join(folder_path, file_name)
            os.remove(temp_file_path)
            print(f"Usunięto plik tymczasowy: {temp_file_path}")

# Funkcja do wczytywania plików JSON z folderu i tworzenia DataFrame
def load_json_files_from_folder(folder_path):
    data_frames = []
    files_status = []  # Do przechowywania statusu każdego pliku
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            temp_file_path = remove_first_and_last_lines(file_path)
            try:
                with open(temp_file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    if content.strip():  # Sprawdź, czy plik nie jest pusty
                        try:
                            json_data = json.loads(content)  # Użyj json.loads na wczytanym tekście
                            
                            # Debugging: log the content of the JSON data
                            print(f"\nZawartość JSON w pliku {file_name}:\n{json_data}")

                            # Obsługuje przypadki, gdy klucz 'dzialki' nie istnieje lub zawiera pojedynczy obiekt
                            dzialki = json_data.get('dzialki', [])
                            
                            # Log the content of 'dzialki'
                            print(f"\nZawartość 'dzialki' w pliku {file_name}:\n{dzialki}")

                            # Jeśli dzialki nie jest listą, zamień go na listę
                            if isinstance(dzialki, dict):
                                dzialki = [dzialki]
                                
                            if dzialki:  # Sprawdź, czy lista 'dzialki' nie jest pusta
                                df = pd.DataFrame(dzialki)
                                
                                # Dodaj kolumny z nazwą pliku (bez rozszerzenia) i datą oraz godziną
                                base_name = os.path.splitext(file_name)[0]
                                file_name_formatted = base_name.replace('_', '/')
                                
                                df['nazwa_pliku'] = file_name_formatted
                                # Zbierz datę i godzinę z zawartości pliku JSON
                                file_date = json_data.get('data_stan_z_dnia', datetime.now().strftime('%Y-%m-%d'))
                                file_time = json_data.get('godzina', datetime.now().strftime('%H:%M'))
                                
                                df['data_pliku'] = file_date
                                df['godzina_pliku'] = file_time
                                
                                data_frames.append(df)
                                files_status.append((file_name, 'Przetworzono'))
                            else:
                                files_status.append((file_name, 'Pusta lista "dzialki"'))
                        except json.JSONDecodeError as e:
                            files_status.append((file_name, f'Błąd dekodowania JSON: {e}'))
                    else:
                        files_status.append((file_name, 'Plik pusty'))
            except Exception as e:
                files_status.append((file_name, f'Nieoczekiwany błąd: {e}'))
    
    # Logowanie statusu plików
    print("\nStatus przetwarzania plików:")
    for file_status in files_status:
        print(f"Plik: {file_status[0]}, Status: {file_status[1]}")
    
    return pd.concat(data_frames, ignore_index=True) if data_frames else pd.DataFrame()

# Ścieżki do folderów i plików
input_folder = 'output'
output_folder = 'output'
output_file = os.path.join(output_folder, 'dzialki.xlsx')
sheet_name = 'działki'

# Wczytaj dane z plików JSON w folderze input
df_dzialki = load_json_files_from_folder(input_folder)

# Jeśli DataFrame nie jest pusty, zapisujemy dane do pliku XLSX
if not df_dzialki.empty:
    # Upewnij się, że folder output istnieje
    os.makedirs(output_folder, exist_ok=True)
    
    # Zapisz DataFrame do pliku XLSX, w arkuszu o nazwie 'działki'
    with pd.ExcelWriter(output_file, engine='openpyxl', mode='w') as writer:
        df_dzialki.to_excel(writer, sheet_name=sheet_name, index=False)

    print(f"Dane zostały zapisane do pliku: {output_file}")
else:
    print("Brak danych do zapisania.")

# Usuń pliki tymczasowe
delete_temp_files(input_folder)
