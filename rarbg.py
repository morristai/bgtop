import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List
import time


# TODO: year start with 1XXX will lose resolution, some permutations problem...


class Rarbg:
    def __init__(self, page: int):
        self.header = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
            "sec-fetch-user": "?1",
            "host": "rarbg.to",
            "dnt": "1",
            "connection": "keep-alive",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-TW;q=0.8,zh-CN;q=0.7,zh;q=0.6",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "cookie": "gaDts48g=q8h5pp9t; gaDts48g=q8h5pp9t; skt=HPKFDptzor; skt=HPKFDptzor; tcc; use_alt_cdn=1; expla=2; aby=1",
            "sec-fetch-dest": "document",
            "cache-control": "max-age=0",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "none",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
        }
        self.page = page

    def query(self):
        found = []
        for i in range(1, self.page + 1):
            url = f"https://rarbg.to/torrents.php?category=14%3B17%3B42%3B44%3B45%3B46%3B47%3B48%3B50%3B51%3B52%3B54&order=leechers&by=DESC&page={i}"
            resp = requests.get(url=url, headers=self.header, verify=True, timeout=3)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')
            title = soup.find_all("a", {"onmouseout": "return nd();"})  # type: bs4.element.Tag
            found += title
        return found

    @staticmethod
    def make_queue(title) -> List:
        queue = []
        for i in range(len(title)):
            try:
                cache = re.split(r'.(2\d{3})\.(\d{4}p).', str(title[i]["title"]))
                queue.append(
                    {
                        'movie': cache[0],
                        'year': cache[1],
                        'resolution': cache[2],
                        'compression': cache[3]
                    }
                )
            except IndexError:
                try:
                    cache = re.split(r'.(2\d{3})\.(\d{3}p).', str(title[i]["title"]))
                    queue.append(
                        {
                            'movie': cache[0],
                            'year': cache[1],
                            'resolution': cache[2],
                            'compression': cache[3]
                        }
                    )
                except IndexError:
                    cache = re.split(r'.(\d{4})\.', str(title[i]["title"]))
                    # print(cache)
                    queue.append(
                        {
                            'movie': cache[0],
                            'year': cache[1],
                            'resolution': None,
                            'compression': cache[2]
                        }
                    )
        return queue

    def make_data_frame(self, title):
        queue = self.make_queue(title)
        df = pd.DataFrame(queue)
        return df


if __name__ == "__main__":
    S = Rarbg(page=2)
    origin = S.query()
    df = S.make_data_frame(origin)
    today = time.strftime("%Y-%m-%d")
    df.to_csv(f'./data/rarbg-{today}.csv', index=False)
