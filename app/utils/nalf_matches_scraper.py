from app.utils.scraper import Scraper
from datetime import datetime


class MatchesScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url = None

    def scrape_matches(self, start_date_str, end_date_str, url):
        self.url = url
        content = self.scrape_content(url)
        matches_list = content['table']
        division = content['title']
        data_objects_list = []

        for idx, match in enumerate(matches_list):
            data_object = {
                "id": idx + 1,
                "date": match.find_all('date')[0].text[:-9],
                "teams": match.find_all('a')[1].text.lstrip().split(' — '),
                "result": self.get_match_result(match.find_all('a')[2].text),
            }

            if self.is_date_between(data_object["date"], start_date_str, end_date_str):
                data_objects_list.append(data_object)
        return {'matches': data_objects_list, 'division': division}

    @staticmethod
    def get_match_result(_data):
        if ' - ' in _data:
            score_a, score_b = _data.split(' - ')
            return f'{score_a}:{score_b}'
        return _data[9:]

    @staticmethod
    def is_date_between(date_str, start_date_str, end_date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        return start_date <= date <= end_date


# # Przykład użycia klasy
# url_to_scrape = 'http://nalffutsal.pl/?page_id=34' # A
# url_to_scrape = 'http://nalffutsal.pl/?page_id=52' # B
# scraper = MatchesScraper(url_to_scrape)
# last_matches = scraper.scrape_matches('2024-01-15', '2024-01-18')
# print('------')
# print('poprzednia kolejka:')
# print('------')
# for match in last_matches['matches']:
#     for data in match:
#         print(f'{data}: {match[data]}')
#     print('------')
#
# future_matches = scraper.scrape_matches('2024-01-23', '2024-01-24')
# print('następna kolejka:')
# print('------')
# for match in future_matches['matches']:
#     for data in match:
#         print(f'{data}: {match[data]}')
#     print('------')


# file_generator = JSONFileGenerator(data_objects)
# file_generator.generate_and_save_file('matches-a.json')
# # file_generator.generate_and_save_file('matches-b.json')

