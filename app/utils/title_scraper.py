from app.utils.scraper import Scraper


class TitleScraper(Scraper):
    def __init__(self):
        super().__init__()
        self.url = None

    def scrape_title(self, url):
        print(url, flush=True)
        self.url = url
        title = self.scrape_title_(url)
        return title

