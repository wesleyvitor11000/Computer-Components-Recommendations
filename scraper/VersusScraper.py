import requests
from bs4 import BeautifulSoup as bs4
import pandas as pd
import time
import random
from selenium import webdriver
from enum import Enum

from Scraper import Scraper


class ElementSource(Enum):
    SPECS = 0
    ENTIRE = 1


class VersusScraper(Scraper):
    def __init__(
        self,
        url: str,
        min_delay: float = 0.3,
        max_delay: float = 1,
        max_requisitions_per_proxy=10,
        retry_delay=0.5,
        **kwargs,
    ) -> None:
        super().__init__(url, "https://versus.com", min_delay, max_delay, **kwargs)
        self.retry_delay = retry_delay
        self.requisition_count = 0
        self.max_requisitions_per_proxy = max_requisitions_per_proxy
        self._load_proxies()
        self.proxy_index = 0
        self.current_proxy = self.proxies[0]

        self.browser = webdriver.Firefox()

    def close_scraper(self):
        self.browser.close()

    def scrape_common_elements(
        self,
        split_into=None,
        remove_components_without_price=True,
        explore_pages=True,
        max_page_num=None,
    ):
        if not explore_pages:
            return self._scrape_common_elements(
                self.url, split_into, remove_components_without_price
            )
        else:
            i = 1
            components_dicts = []
            while True:
                page_url = f"{self.url}?page={i}"
                print(page_url)

                try:
                    components_dicts.extend(
                        self._scrape_common_elements(
                            page_url, split_into, remove_components_without_price
                        )
                    )
                except Exception as e:
                    print(e)
                    print(f"terminou na página {i-1}")
                    break

                if max_page_num and i >= max_page_num:
                    break

                i += 1

                time.sleep(random.uniform(self.min_delay, self.max_delay))

            return components_dicts

    def _scrape_common_elements(
        self, page_url, split_into=None, remove_components_without_price=True
    ):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }
        s = requests.Session()
        html = s.get(page_url, headers=headers)

        soup = bs4(html.content, "html.parser")

        components_table = soup.find(id="mouchoContent")

        components_elements = components_table.select("[data-cy='mouchoListItem']")

        if len(components_elements) <= 0:
            raise Exception("Elemento não encontrado.")

        components_dicts = []

        for ce in components_elements:
            component_name = ce.select("[data-cy='mouchoItemName']")[0].text
            component_mark = ce.find("span", class_="pointsText").find("span").text
            component_href = ce.find("a")["href"]
            component_link = f"{self.domain}{component_href}"

            component_dict = {
                "name": component_name,
                "mark": component_mark,
                "link": component_link,
            }

            components_dicts.append(component_dict)

        return components_dicts

    def _load_proxies(self, file: str = "res/proxies.txt"):
        with open(file, "r") as file:
            self.proxies = file.readlines()
            self.proxies = [p[:-1] for p in self.proxies]

    def _next_proxy(self):
        self.proxy_index = (self.proxy_index + 1) % len(self.proxies)
        self.current_proxy = self.proxies[self.proxy_index]

    def scrape_specific_elements(self, page_url, data_to_colect: dict, max_tries=15):
        self.requisition_count += 1
        wait_time = random.uniform(self.min_delay, self.max_delay)

        if self.requisition_count > self.max_requisitions_per_proxy:
            self.requisition_count = 0
            self._next_proxy()

        begin_time = time.time()
        self.browser.get(page_url)
        end_time = time.time()

        elapsed_time = end_time - begin_time

        if elapsed_time < wait_time:
            time.sleep(wait_time - elapsed_time)

        html = self.browser.page_source
        soup = bs4(html, "html.parser")

        component_infos = {}

        for element_type, elements in data_to_colect.items():
            for atribute_name, element_propertys in elements.items():
                tries = 0
                while tries < max_tries:
                    try:
                        query = f'[{element_type}="{element_propertys[0]}"]'
                        value = soup.select_one(query)

                        [
                            value := value.next_element
                            for _ in range(element_propertys[1])
                        ]

                        if "unknown" in value.text.lower():
                            raise Exception("atributo não informado")

                        component_infos[atribute_name] = value.text
                        break
                    except Exception as e:
                        component_infos[atribute_name] = "NaN"

                        if not element_propertys[2]:
                            break

                        time.sleep(self.retry_delay)

                        html = self.browser.page_source
                        soup = bs4(html, "html.parser")

                        tries += 1

        return component_infos
