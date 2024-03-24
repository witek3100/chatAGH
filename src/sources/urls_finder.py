import json

from usp.tree import sitemap_tree_for_homepage
from src.utils import sources

def get_pages_from_sitemap(domain):
  """
  Extracts URLs from a website's sitemap.
  """
  try:
      all_pages = []
      tree = sitemap_tree_for_homepage(domain)
      for page in tree.all_pages():
        all_pages.append(page.url)
  except Exception as e:
      print(f"Error while fetching url's for domain {domain}: {e}")
      return []

  return all_pages


if __name__ == "__main__":
    domains = [
        'https://www.agh.edu.pl',
        'https://rekrutacja.agh.edu.pl',
        'https://www.eaiib.agh.edu.pl',
        'https://www.wggios.agh.edu.pl',
        'https://www.metal.agh.edu.pl',
        'https://imir.agh.edu.pl',
        'https://odlewnictwo.agh.edu.pl',
        'https://wilgz.agh.edu.pl',
        'https://www.ceramika.agh.edu.pl',
        'https://wnig.agh.edu.pl',
        'http://www.ftj.agh.edu.pl',
        'https://www.wms.agh.edu.pl',
        'https://www.zarz.agh.edu.pl',
        'https://weip.agh.edu.pl',
        'https://iet.agh.edu.pl',
        'https://wh.agh.edu.pl',
        'https://www.sjo.agh.edu.pl',
        'https://www.swfis.agh.edu.pl',
        'https://sylabusy.agh.edu.pl',
        'https://sylabusy.agh.edu.pl/pl/'
        'https://skn.agh.edu.pl',
        'https://dss.agh.edu.pl',
        'https://akademik.agh.edu.pl'
    ]

    def format_link(link: str):
        return link.split('#')[0]

    def filter(page):
        for year in range(16, 22):
            if f'20{str(year)}' in page:
                return True
        if len(page) > 110:
            return True

        return False

    pages = []
    for domain in domains:
        new_links = [format_link(page) for page in get_pages_from_sitemap(domain) if not filter(page)]
        pages.extend(new_links)
        print(f"{len(new_links)} url's found in domain {domain}")

    sources['html'] = list(set(pages))

    json_string = json.dumps(sources, indent=4)
    with open("src/sources/sources.json", "w") as outfile:
        outfile.write(json_string)
    print('done')

