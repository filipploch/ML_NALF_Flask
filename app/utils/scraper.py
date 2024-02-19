from urllib.request import urlopen
from bs4 import BeautifulSoup


class Scraper:
    def __init__(self):
        self.html_content = None

    def _get_html_content(self, url):
        try:
            with urlopen(url) as response:
                content = response.read().decode('utf-8')
            return content
        except print("Error fetching HTML content:"):
            return None

    def scrape_content(self, url, table_index=0):
        self.html_content = self._get_html_content(url)
        if self.html_content:
            # Utwórz obiekt BeautifulSoup
            soup = BeautifulSoup(self.html_content, 'html.parser')


            # Znajdź div o podanym id
            primary_div = soup.find('div', {'id': 'primary'})

            # Sprawdź, czy div istnieje
            if primary_div:
                # Znajdź tabelę wewnątrz diva
                title = primary_div.find('h1', {'class': 'entry-title'}).text
                tables = primary_div.find_all('tbody')
                try:
                    division = primary_div.find_all('h4')[1].text
                except:
                    division = ''
                # Sprawdź, czy istnieje tabela o podanym indeksie
                if table_index < len(tables):
                    table = tables[table_index]
                    # Znajdź wszystkie wiersze w tabeli
                    rows = table.find_all('tr')
                    return {'title': title, 'table': rows, 'division': division}


                else:
                    print(f"Nie znaleziono tabeli o indeksie {table_index} w divie o id='{'primary'}'")
            else:
                print("Nie znaleziono diva o id='primary'")
        else:
            print("Brak HTML content. Sprawdź poprawność URL lub połączenie internetowe.")


