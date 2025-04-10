import requests
import logging
from lxml import etree
import json

class SoundCloud:
    """
    Надає мінімалістичний інтерфейс до SoundCloud API для пошуку та завантаження треків.
    """

    def __init__(self, client_id):
        self.client_id = client_id
        self.base_url = "https://api.soundcloud.com"
        self.HTMLParser = etree.HTMLParser()
        self._build_browser()

    def _build_browser(self):
        """Ініціалізація браузера для обробки запитів"""
        self.browser = requests.Session()
        self.browser.headers.update({"User-Agent": "Mozilla/5.0"})

    def url(self, endpoint):
        """Формуємо URL для доступу до SoundCloud API"""
        return f"{self.base_url}{endpoint}?client_id={self.client_id}"

    def find_track_id(self, url):
        """
        Знаходимо track_id для пісні з профілю SoundCloud.
        """
        response = self.browser.get(url)
        tree = etree.HTML(response.text, self.HTMLParser)
        try:
            track_url = tree.xpath("//meta[contains(@content, 'https://w.soundcloud.com')]")[0]
        except IndexError:
            track_url = None

        if track_url is not None:
            track_id = track_url.attrib["content"].split("%2Ftracks%2F")[1].split("&")[0]
            return track_id
        return None

    def get_track_info(self, track_id):
        """
        Отримуємо інформацію про трек за допомогою SoundCloud API
        """
        url = self.url(f"/tracks/{track_id}/")
        response = self.browser.get(url)
        return json.loads(response.text)

    def download_track(self, track_id):
        """
        Завантажуємо трек через SoundCloud API.
        """
        url = self.url(f"/tracks/{track_id}/download")
        response = self.browser.get(url)
        with open(f"track_{track_id}.mp3", "wb") as file:
            file.write(response.content)
        logging.info(f"Завантажено трек: {track_id}")

    def download_song(self, url):
        """
        Основна функція для завантаження пісні.
        """
        track_id = self.find_track_id(url)
        if track_id:
            track_info = self.get_track_info(track_id)
            if track_info and track_info.get('downloadable', False):
                logging.info(f"[Завантаження] {track_info['title']}...")
                self.download_track(track_id)
            else:
                logging.error("[Помилка] Файл недоступний для завантаження.")
        else:
            logging.error("[Помилка] Трек не знайдено.")
