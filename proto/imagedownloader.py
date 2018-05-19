try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


class ImageDownloader:
    def __init__(self):
        self.visited = set()
        self.session = requests.Session()
        self.session.headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.109 Safari/537.36"}

        requests.packages.urllib3.disable_warnings()  # turn off SSL warnings

    def visit_url(self, url, level):
        #print(url)
        if self.is_image_url(url):
            self.download_image(url, "")
            return
        if url in self.visited:
            return

        self.visited.add(url)

        content = self.session.get(url, verify=False).content
        soup = BeautifulSoup(content, "lxml")

        for img in soup.select("img[src]"):
            image_url = img["src"]
            if not image_url.startswith(("data:image", "javascript")):
                self.download_image(urljoin(url, image_url), "")

        if level > 0:
            for link in soup.select("a[href]"):
                self.visit_url(urljoin(url, link["href"]), level - 1)

    def is_image_url(self, image_url):
        valid_extensions = [".png", ".jpg", ".jpeg", ".gif"]
        for exp in valid_extensions:
            if image_url.endswith(exp):
                return True
        return False

    def download_image(self, image_url, image_dir):
        if self.is_image_url(image_url):
            local_filename = image_url.split('/')[-1].split("?")[0]

            r = self.session.get(image_url, stream=True, verify=False)
            with open("images/" + local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)