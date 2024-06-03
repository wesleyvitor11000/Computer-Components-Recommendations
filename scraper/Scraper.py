from abc import ABC
from abc import abstractmethod


class Scraper(ABC):
    def __init__(
        self,
        url: str,
        domain: str,
        min_delay: float = 0,
        max_delay: float = 1,
        **kwargs,
    ) -> None:
        super().__init__()
        self.domain = domain
        self.url = url
        self.min_delay = min_delay
        self.max_delay = max_delay

    @abstractmethod
    def scrape_common_elements(
        self, split_into=None, remove_components_without_price=True
    ):
        pass
