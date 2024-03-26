import asyncio
import aiohttp
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

class DomainScrapper:
    def __init__(self, url):
        self.url = url
        self.domain = self._get_domain(self.url)

    def _get_links(self, html, url):
        soup = BeautifulSoup(html, 'lxml')
        links = set()
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url:
                absolute_link = urljoin(url, link_url)
                if absolute_link.startswith(self.domain):
                    links.add(absolute_link)
        return links

    def _get_domain(self, url):
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain

    def _filter(self, page):
        for year in range(16, 22):
            if f'20{str(year)}' in page:
                return False
        if len(page) > 110:
            return False
        return True

    async def _get_links_async(self, session, url):
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text(encoding='utf-8', errors='ignore')
                    result = self._get_links(html, url)
                    return result
                else:
                    return set()
        except aiohttp.ClientConnectorError as e:
            print(f"Error connecting to {url}: {e}")
            return set()
        except aiohttp.ServerDisconnectedError as e:
            print(f"Server disconnected while accessing {url}: {e}")
            return set()
        except Exception as e:
            print(f"Error occured while loading {url}: {e}")
            return set()

    async def scrap_async(self):
        scraped_urls = []

        try:
            print(f'scraping {self.domain} ...')

            queue = [self.url]
            visited = set()

            async with aiohttp.ClientSession() as session:
                while queue:
                    tasks = []
                    for url in queue:
                        tasks.append(self._get_links_async(session, url))
                    results = await asyncio.gather(*tasks)

                    for links in results:
                        for link in links:
                            if link not in visited and link not in queue:
                                queue.append(link)
                                visited.add(link)

                    queue = queue[1:]  # Remove the first element

            urls = [url for url in visited if self._filter(url)]
            print(f'{len(urls)} urls found in domain: {self.domain}')
            scraped_urls.extend(urls)
        except Exception as e:
            print(f'Error scraping domain {self.domain}: {e}')

        return scraped_urls

if __name__ == '__main__':
    async def main():
        urls = await DomainScrapper('https://www.agh.edu.pl').scrap_async()
        print(urls)

    asyncio.run(main())
