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
        'https://rekrutacja.agh.edu.pl'
    ]
    pages = []
    for domain in domains:
        pages.extend(get_pages_from_sitemap(domain))
    sources['html'] = pages

    print(f"{len(pages)} url's found in domains {domains}")

    json_string = json.dumps(sources, indent=4)
    with open("src/sources/sources.json", "w") as outfile:
        outfile.write(json_string)

