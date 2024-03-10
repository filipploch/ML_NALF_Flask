from app.utils.scraper import Scraper


class ScorersScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url = None

    def scrape_best_scorers(self, url, _type):
        self.url = url
        rows = self.scrape_content(url)['table']
        data_objects_list = []
        for row in rows:
            data_object = {
                'rank': row.find('td', class_='data-rank').text,
                'name': row.find('td', class_='data-name').text,
                'team': row.find('td', class_='data-team').text,
                'points': row.find('td', class_=f'data-{_type}').text
            }
            data_objects_list.append(data_object)
        print(data_objects_list)
        return data_objects_list[:10]
