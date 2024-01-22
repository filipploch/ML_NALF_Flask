from app.utils.scraper import Scraper


class TableScraper(Scraper):
    def __init__(self, url):
        super().__init__(url)

    def scrape_league_table(self):
        rows = self.scrape_content()['table']
        data_objects_list = []
        for row in rows:
            data_object = {
                'rank': row.find('td', class_='data-rank').text,
                'name': row.find('a').text,
                'team_logo': self._get_team_logo_name_from_link(row),
                'matches': int(row.find('td', class_='data-m').text),
                'wins': int(row.find('td', class_='data-z').text),
                'draws': int(row.find('td', class_='data-r').text),
                'lost': int(row.find('td', class_='data-p').text),
                'goals_scored': int(row.find('td', class_='data-gz').text),
                'goals_lost': int(row.find('td', class_='data-gs').text),
                'points': int(row.find('td', class_='data-pkt').text)
            }
            data_objects_list.append(data_object)
        return data_objects_list

    def _get_team_logo_name_from_link(self, link):
        return link.select_one('.data-name img')['src'].split('/')[-1].split('.')[0]


# url_to_scrape = 'http://nalffutsal.pl/?page_id=16'
# scraper = TableScraper(url_to_scrape)
# data_objects = scraper.scrape_league_table()
#
# for o in data_objects:
#     print(o['team_logo'])