import requests
from bs4 import BeautifulSoup
import pandas as pd

from .Scraper import Scraper


class PassMarkScraper(Scraper):
    def scrape_common_elements(
        self, split_into=None, remove_components_without_price=True
    ):
        html = requests.get(self.url)
        soup = BeautifulSoup(html.content, "html.parser")

        components_table = soup.find("tbody")
        components_elements = components_table.find_all("tr")

        components = []

        for component_element in components_elements:
            component_columns = component_element.findAll("td")
            component_price = component_columns[-1].text

            if component_price == "NA" and remove_components_without_price:
                continue

            component_mark = component_columns[1].text
            component_rank = component_columns[2].text

            component_id = component_element["id"]
            component_name = component_element.find("a").text

            if split_into:
                component_name = component_name.split(split_into)[0]

            component = {
                "id": component_id,
                "name": component_name,
                "rank": component_rank,
                "mark": component_mark,
                "price": component_price,
            }

            components.append(component)

        print(f"{len(components)} componentes.")

        writer = pd.ExcelWriter("test.xlsx")

        pd_t = pd.DataFrame(components)
        pd_t.to_excel(writer)
        print(pd_t)
        writer.close()


# request -> bs4 -> pandas -> csv -> classes
