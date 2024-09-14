import os
import requests
import json

# Konfiguracja
api_key = "API_KEY__________________________________________________________"
base_url = "https://api.openai.com/v1/chat/completions"
model_name = "gpt-4o-mini"
input_folder = 'input'
output_folder = 'output'

# Wczytaj zawartość pliku HTML
def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Przygotuj zapytanie do API OpenAI
def send_to_openai(prompt):
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    data = {
        'model': model_name,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 4096
    }
    
    response = requests.post(base_url, headers=headers, json=data)
    return response.json()

# Zapisz odpowiedź do pliku
def save_response_to_file(filename, content):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    output_file_path = os.path.join(output_folder, filename.replace('.html', '.txt'))
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Przetwarzaj pliki HTML w folderze
def process_html_files(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)
            html_content = read_html_file(file_path)
            
            # Utwórz prompt dla modelu
            prompt = (
                "Analizuj poniższy dokument HTML i wyodrębnij  z nich numer działki, identyfikator działki,     województwo,  powiat,  gmina,  miejscowość, ulica, sposób korzystania. Nie dodawaj swoich komentarzy, nie używaj znaków *. Używaj formatowania JSON. Przypisz pola tylko gdy masz ich pewność np. jeśli identyfikator działki nie jest jawnie określony to pomiń to pole. Numer działki jest jeden dla każdej z pozyczji i może to być np. 100, 10/231, 40/4131. Przykładowy identyfikator działki to 140504_4.0023.118/1. Dla każdej pozycji twórz klucz główny 'dzialki'. W nazwach pozycji nie używaj polskich znaków ani spacji, używaj np. identyfikator_dzialki, wojewodztwo, numer_dzialki, sposob_korzystania itp."
                 
                 
                f"Dokument HTML:\n{html_content}"
            )
            
            # Wyślij zapytanie do OpenAI
            response = send_to_openai(prompt)
            
            # Wyodrębnij zawartość odpowiedzi
            if 'choices' in response and len(response['choices']) > 0:
                content = response['choices'][0]['message']['content']
                print(filename, content)
            else:
                content = "Brak odpowiedzi lub błąd zapytania"
            
            # Zapisz odpowiedź do pliku
            save_response_to_file(filename, content)
            print(f"Response for {filename} saved to {filename.replace('.html', '.txt')}")

# Przykładowa funkcja main
def main():
    process_html_files(input_folder)

if __name__ == '__main__':
    main()
