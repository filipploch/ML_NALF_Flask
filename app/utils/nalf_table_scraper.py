from app.utils.scraper import Scraper


class TableScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url = None

    def scrape_league_table(self, url):
        self.url = url
        rows = self.scrape_content(url)['table']
        data_objects_list = []
        for row in rows:
            data_object = {
                'rank': row.find('td', class_='data-rank').text,
                'name': row.find('a').text,
                'logo_file': row.select_one('.data-name img')['src'],
                'link': row.select_one('.data-name a')['href'],
                'matches': int(row.find('td', class_='data-m').text),
                'wins': int(row.find('td', class_='data-z').text),
                'draws': int(row.find('td', class_='data-r').text),
                'lost': int(row.find('td', class_='data-p').text),
                'goals_scored': int(row.find('td', class_='data-gz').text),
                'goals_lost': int(row.find('td', class_='data-gs').text),
                'points': int(row.find('td', class_='data-pkt').text)
            }
            data_object.update({'goals_difference': data_object['goals_scored'] - data_object['goals_lost']})
            data_objects_list.append(data_object)
        return data_objects_list

# TO DZIAŁA!!!
# url_to_scrape = 'http://nalffutsal.pl/?page_id=16'
# scraper = TableScraper(url_to_scrape)
# data_objects = scraper.scrape_league_table()
#
# for team in data_objects:
#     for data in team:
#         print(f'{data}: {team[data]}')
#     print('------')
